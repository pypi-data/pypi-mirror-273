use std::{borrow::Cow, env::set_current_dir, fs, io, path::Path, process::Command, string};

const FLATC_BINARY: &str = if cfg!(windows) { "flatc.exe" } else { "flatc" };
const OUT_FOLDER: &str = "./src/generated";
const SCHEMA_FOLDER: &str = "./flatbuffers-schema";
const SCHEMA_FOLDER_BACKUP: &str = "../flatbuffers-schema";

const PYTHON_OUT_FOLDER: &str = "./src/python";

#[derive(Debug, PartialEq, Eq)]
enum PythonBindType {
    Struct,
    Enum,
    Union,
}

struct PythonBindGenerator {
    filename: String,
    struct_name: String,
    struct_t_name: String,
    types: Vec<Vec<String>>,
    file_contents: Vec<Cow<'static, str>>,
    bind_type: PythonBindType,
    has_complex_pack: bool,
}

impl PythonBindGenerator {
    const BASE_TYPES: [&'static str; 6] = ["bool", "i32", "u32", "f32", "String", "u8"];
    const SPECIAL_BASE_TYPES: [&'static str; 2] = ["FloatT", "BoolT"];

    fn new(path: &Path) -> Option<Self> {
        // get the filename without the extension
        let filename = path.file_stem().unwrap().to_str().unwrap();

        if filename == "mod" {
            return None;
        }

        // convert snake_case to CamelCase to get the struct name
        let mut struct_name = String::new();
        for c in filename.split('_') {
            struct_name.push_str(&c[..1].to_uppercase());
            struct_name.push_str(&c[1..]);
        }
        struct_name = struct_name
            .replace("Rlbot", "RLBot")
            .replace("Halign", "HAlign")
            .replace("Valign", "VAlign");

        let struct_t_name = format!("{struct_name}T");

        let contents = fs::read_to_string(path).ok()?;

        #[cfg(windows)]
        let contents = contents.replace("\r\n", "\n");

        let Some((types, bind_type)) = Self::get_normal_struct_types(&contents, &struct_t_name)
            .or_else(|| Self::get_enum_struct_types(&contents, &struct_name))
        else {
            println!("Could not find struct definition in {filename} for {struct_t_name}");
            return None;
        };

        let has_complex_pack = contents.contains("pub fn pack<'b, A: flatbuffers::Allocator + 'b>(");
        let mut file_contents = vec![];

        file_contents.push(Cow::Borrowed(match bind_type {
            PythonBindType::Struct => "use crate::{flat_err_to_py, generated::rlbot::flat, FromGil, IntoGil};",
            PythonBindType::Union => "use crate::{generated::rlbot::flat, FromGil, IntoGil};",
            PythonBindType::Enum => "use crate::{flat_err_to_py, generated::rlbot::flat};",
        }));

        if bind_type != PythonBindType::Union {
            if has_complex_pack {
                file_contents.push(Cow::Borrowed("use flatbuffers::{root, FlatBufferBuilder};"));
            } else {
                file_contents.push(Cow::Borrowed("use flatbuffers::root;"));
            }
        }

        if bind_type == PythonBindType::Struct && has_complex_pack {
            file_contents.push(Cow::Borrowed("use get_size::GetSize;"));
        }

        file_contents.push(Cow::Borrowed(match bind_type {
            PythonBindType::Struct => "use pyo3::{pyclass, pymethods, types::PyBytes, Bound, Py, PyResult, Python};",
            PythonBindType::Enum => {
                "use pyo3::{exceptions::PyValueError, pyclass, pymethods, types::PyBytes, Bound, PyResult, Python};"
            }
            PythonBindType::Union => "use pyo3::{pyclass, pymethods, Py, PyObject, Python, ToPyObject};",
        }));

        file_contents.push(Cow::Borrowed(""));

        Some(Self {
            filename: filename.to_string(),
            struct_name,
            struct_t_name,
            types,
            file_contents,
            bind_type,
            has_complex_pack,
        })
    }

    fn add_get_size_derive(&self, path: &Path) {
        let mut contents = fs::read_to_string(path).unwrap();

        #[cfg(windows)]
        {
            contents = contents.replace("\r\n", "\n");
        }

        contents = contents.replace("use self::flatbuffers", "use get_size::GetSize;\nuse self::flatbuffers");

        match self.bind_type {
            PythonBindType::Struct => {
                contents = contents.replace(
                    "#[derive(Debug, Clone, PartialEq)]\n",
                    "#[derive(Debug, Clone, PartialEq, GetSize)]\n",
                );

                contents = contents.replace(
                    "#[derive(Debug, Clone, PartialEq, Default)]\n",
                    "#[derive(Debug, Clone, PartialEq, Default, GetSize)]\n",
                );
            }
            PythonBindType::Union => {
                contents = contents.replace(
                    "#[derive(Debug, Clone, PartialEq)]\n",
                    "#[derive(Debug, Clone, PartialEq, GetSize)]\n",
                );
            }
            PythonBindType::Enum => {
                contents = contents.replace(
                    "#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default)]\n",
                    "#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default, GetSize)]\n",
                );
            }
        }

        fs::write(path, contents).unwrap();
    }

    fn get_enum_struct_types(contents: &str, struct_name: &str) -> Option<(Vec<Vec<String>>, PythonBindType)> {
        let struct_definition = format!("pub struct {struct_name}(pub u8);\n");
        let struct_pos = contents.find(&struct_definition)?;

        // find 'impl CollisionShape {\n'
        let impl_definition = format!("impl {struct_name} {{\n");
        let impl_pos = contents[struct_pos..].find(&impl_definition)?;

        // the next lines should be in the format 'pub const {some value}: Self = Self(i);\n'
        let mut file_line_start = struct_pos + impl_pos + impl_definition.len();
        let mut lines = contents[file_line_start..].split('\n');
        let mut types = Vec::new();

        loop {
            let line = lines.next()?;
            let line_trim = line.trim();

            if line_trim.is_empty() {
                break;
            }

            if line_trim.starts_with("//") {
                file_line_start += line.len();
                continue;
            }

            let definition = line_trim.trim_start_matches("pub const ").trim_end_matches(';');

            let mut parts = definition.split(": Self = ");

            let variable_name = parts.next()?;
            let variable_value = parts.next()?.trim_start_matches("Self(").trim_end_matches(')');

            types.push(vec![variable_name.to_string(), variable_value.to_string()]);

            file_line_start += line.len();
        }

        if types.is_empty() {
            return None;
        }

        let union_definition = format!("pub enum {struct_name}T {{\n");
        let Some(union_start) = contents.find(&union_definition) else {
            return Some((types, PythonBindType::Enum));
        };

        let union_end_definition = "}\n";
        let union_end = contents[union_start..].find(union_end_definition).unwrap();

        let union_definition =
            &contents[union_start + union_definition.len()..union_start + union_end - union_end_definition.len()];

        for (line, variables) in union_definition.split('\n').zip(&mut types) {
            let variable_name = variables[0].as_str();

            let line_trim = line.trim().trim_start_matches(variable_name).trim_end_matches(',');

            if line_trim.is_empty() {
                variables[1].clear();
                continue;
            }

            variables.push(camel_to_snake_case(variable_name));

            let new_type = line_trim.trim_start_matches("(Box<").trim_end_matches("T>)");
            variables[1] = new_type.to_string();
        }

        Some((types, PythonBindType::Union))
    }

    fn get_normal_struct_types(contents: &str, struct_t_name: &str) -> Option<(Vec<Vec<String>>, PythonBindType)> {
        // find the struct definition
        let struct_start_definition = format!("pub struct {struct_t_name} {{\n");
        let struct_start = contents.find(&struct_start_definition)?;

        let struct_end_definition = "}\n";
        let struct_end = contents[struct_start..].find(struct_end_definition).unwrap();

        let start = struct_start + struct_start_definition.len();
        let end = struct_start + struct_end - struct_end_definition.len();

        if end <= start {
            return Some((Vec::new(), PythonBindType::Struct));
        }

        let struct_definition = &contents[start..end];

        Some((
            struct_definition
                .split('\n')
                .map(|s| {
                    s.trim_start_matches(' ')
                        .trim_start_matches("pub ")
                        .trim_end_matches(',')
                        .split(": ")
                        .map(string::ToString::to_string)
                        .collect()
                })
                .collect(),
            PythonBindType::Struct,
        ))
    }

    fn write_str(&mut self, s: &'static str) {
        self.file_contents.push(Cow::Borrowed(s));
    }

    fn write_string(&mut self, s: String) {
        self.file_contents.push(Cow::Owned(s));
    }

    fn generate_struct_definition(&mut self) {
        self.write_str("#[pyclass(module = \"rlbot_flatbuffers\", subclass, get_all, set_all)]");

        if self.types.is_empty() {
            self.write_str("#[derive(Debug, Default, Clone)]");
            self.write_string(format!("pub struct {} {{}}", self.struct_name));
            self.write_str("");
            return;
        }

        self.write_str("#[derive(Debug, Clone)]");
        self.write_string(format!("pub struct {} {{", self.struct_name));

        for variable_info in &self.types {
            let variable_name = &variable_info[0];
            let mut variable_type = variable_info[1].to_string();

            if variable_type.starts_with("Vec<") && variable_type.ends_with("T>") {
                variable_type = format!(
                    "Vec<Py<super::{}>>",
                    variable_type.trim_start_matches("Vec<").trim_end_matches("T>")
                );
            } else if variable_type.starts_with("Vec<") && variable_type.ends_with('>') {
                variable_type = String::from("Py<PyBytes>");
            } else if variable_type.starts_with("Box<") && variable_type.ends_with('>') {
                variable_type = format!(
                    "Py<super::{}>",
                    variable_type
                        .trim_start_matches("Box<")
                        .trim_end_matches('>')
                        .trim_end_matches('T')
                );
            } else if variable_type.starts_with("Option<") && variable_type.ends_with('>') {
                let inner_type = variable_type
                    .trim_start_matches("Option<")
                    .trim_start_matches("Box<")
                    .trim_end_matches('>')
                    .trim_end_matches('T');

                if Self::BASE_TYPES.contains(&inner_type) {
                    variable_type = format!("Option<{inner_type}>");
                } else {
                    variable_type = format!("Option<Py<super::{inner_type}>>");
                }
            } else if variable_type.ends_with('T') {
                variable_type = format!("Py<super::{}>", variable_type.trim_end_matches('T'));
            } else if !Self::BASE_TYPES.contains(&variable_type.as_str()) {
                variable_type = format!("super::{variable_type}");
            }

            self.file_contents
                .push(Cow::Owned(format!("    pub {variable_name}: {variable_type},")));
        }

        self.write_str("}");
        self.write_str("");
        self.write_string(format!("impl crate::PyDefault for {} {{", self.struct_name));
        self.write_str("    fn py_default(py: Python) -> Py<Self> {");
        self.write_str("        Py::new(py, Self {");

        for variable_info in &self.types {
            let variable_name = &variable_info[0];
            let variable_type = &variable_info[1];

            if variable_type.starts_with("Vec<") {
                self.file_contents.push(Cow::Owned(if variable_type == "Vec<u8>" {
                    format!("            {variable_name}: PyBytes::new_bound(py, &[]).unbind(),")
                } else {
                    format!("            {variable_name}: Vec::new(),")
                }));
            } else if variable_type.starts_with("Option<") {
                self.file_contents
                    .push(Cow::Owned(format!("            {variable_name}: None,")));
            } else if !Self::BASE_TYPES.contains(&variable_type.as_str())
                && (variable_type.starts_with("Box<") || variable_type.ends_with('T'))
            {
                let inner_type = variable_type
                    .trim_start_matches("Box<")
                    .trim_end_matches('>')
                    .trim_end_matches('T');

                self.file_contents.push(Cow::Owned(format!(
                    "            {variable_name}: Py::new(py, super::{inner_type}::py_default(py)).unwrap(),"
                )));
            } else {
                self.file_contents
                    .push(Cow::Owned(format!("            {variable_name}: Default::default(),")));
            }
        }

        self.write_str("        }).unwrap()");
        self.write_str("    }");
        self.write_str("}");
        self.write_str("");
    }

    fn generate_enum_definition(&mut self) {
        self.write_str("#[allow(non_camel_case_types)]");
        self.write_str("#[pyclass(module = \"rlbot_flatbuffers\", get_all, set_all)]");
        self.write_str("#[derive(Debug, Default, Clone, Copy)]");
        self.write_string(format!("pub enum {} {{", self.struct_name));
        self.write_str("    #[default]");

        for variable_info in &self.types {
            let variable_name = &variable_info[0];
            let variable_value = &variable_info[1];

            self.file_contents
                .push(Cow::Owned(format!("    {variable_name} = {variable_value},")));
        }

        self.write_str("}");
        self.write_str("");
    }

    fn generate_definition(&mut self) {
        match self.bind_type {
            PythonBindType::Enum => self.generate_enum_definition(),
            PythonBindType::Struct => self.generate_struct_definition(),
            PythonBindType::Union => self.generate_union_definition(),
        }
    }

    fn generate_union_definition(&mut self) {
        self.write_str("#[derive(Debug, Clone, pyo3::FromPyObject)]");
        self.write_string(format!("pub enum {}Union {{", self.struct_name));

        for variable_info in self.types.iter().skip(1) {
            let variable_name = &variable_info[0];
            self.file_contents
                .push(Cow::Owned(format!("    {variable_name}(Py<super::{variable_name}>),")));
        }

        self.write_str("}");
        self.write_str("");
        self.write_str("#[pyclass(module = \"rlbot_flatbuffers\")]");
        self.write_str("#[derive(Debug, Default, Clone)]");
        self.write_string(format!("pub struct {} {{", self.struct_name));
        self.write_str("    #[pyo3(set)]");
        self.write_string(format!("    pub item: Option<{}Union>,", self.struct_name));
        self.write_str("}");
        self.write_str("");
    }

    fn generate_from_flat_impls(&mut self) {
        match self.bind_type {
            PythonBindType::Enum => self.generate_enum_from_flat_impls(),
            PythonBindType::Struct => self.generate_struct_from_flat_impls(),
            PythonBindType::Union => self.generate_union_from_flat_impls(),
        }
    }

    fn generate_union_from_flat_impls(&mut self) {
        let from_impl_types = [
            format!("flat::{}", self.struct_t_name),
            format!("Box<flat::{}>", self.struct_t_name),
        ];

        for impl_type in from_impl_types {
            self.write_string(format!("impl FromGil<{impl_type}> for Py<{}> {{", self.struct_name));
            self.write_string(format!("    fn from_gil(py: Python, flat_t: {impl_type}) -> Self {{"));

            if impl_type.starts_with("Box<") {
                self.write_str("        Self::from_gil(py, *flat_t)");
            } else {
                self.write_str("        Py::new(");
                self.write_str("            py,");
                self.write_str("            match flat_t {");

                for variable_info in &self.types {
                    let variable_name = &variable_info[0];

                    if variable_name == "NONE" {
                        self.file_contents.push(Cow::Owned(format!(
                            "                flat::{}::NONE => {}::default(),",
                            self.struct_t_name, self.struct_name
                        )));
                    } else {
                        self.file_contents.push(Cow::Owned(format!(
                            "                flat::{}::{variable_name}(item) => {} {{",
                            self.struct_t_name, self.struct_name,
                        )));
                        self.file_contents.push(Cow::Owned(format!(
                            "                    item: Some({}Union::{variable_name}(item.into_gil(py)))",
                            self.struct_name,
                        )));
                        self.file_contents.push(Cow::Borrowed("                },"));
                    }
                }

                self.write_str("            },");
                self.write_str("        )");
                self.write_str("        .unwrap()");
            }

            self.write_str("    }");
            self.write_str("}");
            self.write_str("");
        }
    }

    fn generate_enum_from_flat_impls(&mut self) {
        self.write_string(format!("impl From<flat::{}> for {} {{", self.struct_name, self.struct_name));
        self.write_string(format!("    fn from(flat_t: flat::{}) -> Self {{", self.struct_name));
        self.write_str("        match flat_t {");

        for variable_info in &self.types {
            let variable_name = &variable_info[0];

            self.file_contents.push(Cow::Owned(format!(
                "            flat::{}::{variable_name} => Self::{variable_name},",
                self.struct_name
            )));
        }

        self.write_str("            v => unreachable!(\"Unknown value: {v:?}\"),");

        self.write_str("        }");
        self.write_str("    }");
        self.write_str("}");
        self.write_str("");
    }

    fn generate_struct_from_flat_impls(&mut self) {
        let from_impl_types = [
            format!("flat::{}", self.struct_t_name),
            format!("Box<flat::{}>", self.struct_t_name),
        ];

        for impl_type in from_impl_types {
            self.write_string(format!("impl FromGil<{impl_type}> for Py<{}> {{", self.struct_name));

            if self.types.is_empty() {
                self.write_string(format!("    fn from_gil(py: Python, _: {impl_type}) -> Self {{"));
                self.write_string(format!("        Py::new(py, {}::default()).unwrap()", self.struct_name));
                self.write_str("    }");
                self.write_str("}");
                self.write_str("");
                continue;
            }

            self.write_string(format!("    fn from_gil(py: Python, flat_t: {impl_type}) -> Self {{"));

            if impl_type.starts_with("Box<") {
                self.write_str("        Self::from_gil(py, *flat_t)");
            } else {
                self.write_string(format!("        Py::new(py, {} {{", self.struct_name));

                for variable_info in &self.types {
                    let variable_name = &variable_info[0];
                    let variable_type = variable_info[1].as_str();

                    if variable_type.starts_with("Vec<") {
                        self.file_contents
                                .push(Cow::Owned(if variable_type == "Vec<u8>" {
                            format!("            {variable_name}: PyBytes::new_bound(py, &flat_t.{variable_name}).unbind(),")
                        } else {
                            format!(
                                "            {variable_name}: flat_t.{variable_name}.into_iter().map(|x| x.into_gil(py)).collect(),",
                            )
                        }));
                    } else if variable_type.starts_with("Option<") {
                        self.file_contents.push(Cow::Owned(
                            if variable_type.trim_start_matches("Option<").trim_end_matches('>') == "String" {
                                format!("            {variable_name}: flat_t.{variable_name},")
                            } else {
                                format!("            {variable_name}: flat_t.{variable_name}.map(|x| x.into_gil(py)),")
                            },
                        ));
                    } else if variable_type.starts_with("Box<") || variable_type.ends_with('T') {
                        self.file_contents.push(Cow::Owned(format!(
                            "            {variable_name}: flat_t.{variable_name}.into_gil(py),",
                        )));
                    } else if Self::BASE_TYPES.contains(&variable_type) {
                        self.file_contents
                            .push(Cow::Owned(format!("            {variable_name}: flat_t.{variable_name},")));
                    } else {
                        self.file_contents.push(Cow::Owned(format!(
                            "            {variable_name}: flat_t.{variable_name}.into(),",
                        )));
                    }
                }

                self.write_str("        }).unwrap()");
            }

            self.write_str("    }");
            self.write_str("}");
            self.write_str("");
        }
    }

    fn generate_union_to_flat_impls(&mut self) {
        let from_impl_types = [
            format!("flat::{}", self.struct_t_name),
            format!("Box<flat::{}>", self.struct_t_name),
        ];

        for impl_type in from_impl_types {
            self.write_string(format!("impl FromGil<&Py<{}>> for {impl_type} {{", self.struct_name));
            self.write_string(format!(
                "    fn from_gil(py: Python, py_type: &Py<{}>) -> Self {{",
                self.struct_name
            ));

            if impl_type.contains("Box<") {
                self.write_string(format!(
                    "        Self::new(flat::{}::from_gil(py, py_type))",
                    self.struct_t_name
                ));
            } else {
                self.write_str("        match py_type.borrow(py).item.as_ref() {");
                for variable_info in &self.types {
                    let variable_name = &variable_info[0];
                    let variable_value = &variable_info[1];

                    if variable_value.is_empty() {
                        self.file_contents.push(Cow::Borrowed("            None => Self::NONE,"));
                    } else {
                        self.file_contents.push(Cow::Owned(format!(
                            "            Some({}Union::{variable_value}(item)) => flat::{}::{variable_name}(item.into_gil(py)),",
                            self.struct_name, self.struct_t_name
                        )));
                    }
                }

                self.write_str("        }");
            }

            self.write_str("    }");
            self.write_str("}");
            self.write_str("");
        }
    }

    fn generate_to_flat_impls(&mut self) {
        match self.bind_type {
            PythonBindType::Enum => self.generate_enum_to_flat_impls(),
            PythonBindType::Struct => self.generate_struct_to_flat_impls(),
            PythonBindType::Union => self.generate_union_to_flat_impls(),
        }
    }

    fn generate_enum_to_flat_impls(&mut self) {
        self.write_string(format!("impl From<&{}> for flat::{} {{", self.struct_name, self.struct_name));
        self.write_string(format!("    fn from(py_type: &{}) -> Self {{", self.struct_name));
        self.write_str("        match *py_type {");

        for variable_info in &self.types {
            let variable_name = &variable_info[0];

            self.file_contents.push(Cow::Owned(format!(
                "            {}::{variable_name} => Self::{variable_name},",
                self.struct_name
            )));
        }

        self.write_str("        }");
        self.write_str("    }");
        self.write_str("}");

        self.write_str("");
    }

    fn generate_struct_to_flat_impls(&mut self) {
        let from_impl_types = [
            format!("flat::{}", self.struct_t_name),
            format!("Box<flat::{}>", self.struct_t_name),
        ];

        self.write_string(format!(
            "impl FromGil<&{}> for flat::{} {{",
            self.struct_name, self.struct_t_name
        ));

        if self.types.is_empty() {
            self.write_string(format!("    fn from_gil(_: Python, _: &{}) -> Self {{", self.struct_name));
            self.write_str("        Self::default()");
        } else {
            self.write_str("    #[allow(unused_variables)]");
            self.write_string(format!(
                "    fn from_gil(py: Python, py_type: &{}) -> Self {{",
                self.struct_name
            ));
            self.write_str("        Self {");

            for variable_info in &self.types {
                let variable_name = &variable_info[0];
                let variable_type = variable_info[1].as_str();

                if variable_type.starts_with("Vec<") {
                    self.file_contents.push(Cow::Owned(if variable_type == "Vec<u8>" {
                        format!("            {variable_name}: py_type.{variable_name}.as_bytes(py).to_vec(),")
                    } else {
                        format!(
                            "            {variable_name}: py_type.{variable_name}.iter().map(|x| x.into_gil(py)).collect(),",
                        )
                    }));
                } else if variable_type.starts_with("Option<") {
                    self.file_contents.push(Cow::Owned(
                        if variable_type.trim_start_matches("Option<").trim_end_matches('>') == "String" {
                            format!("            {variable_name}: py_type.{variable_name}.clone(),")
                        } else {
                            format!("            {variable_name}: py_type.{variable_name}.as_ref().map(|x| x.into_gil(py)),")
                        },
                    ));
                } else if variable_type == "String" {
                    self.file_contents.push(Cow::Owned(format!(
                        "            {variable_name}: py_type.{variable_name}.clone(),",
                    )));
                } else if variable_type.ends_with('T') || variable_type.starts_with("Box<") {
                    self.file_contents.push(Cow::Owned(format!(
                        "            {variable_name}: (&py_type.{variable_name}).into_gil(py),",
                    )));
                } else if Self::BASE_TYPES.contains(&variable_type) {
                    self.file_contents
                        .push(Cow::Owned(format!("            {variable_name}: py_type.{variable_name},")));
                } else {
                    self.file_contents.push(Cow::Owned(format!(
                        "            {variable_name}: (&py_type.{variable_name}).into(),",
                    )));
                }
            }

            self.write_str("        }");
        }

        self.write_str("    }");
        self.write_str("}");
        self.write_str("");

        for impl_type in from_impl_types {
            self.write_string(format!("impl FromGil<&Py<{}>> for {impl_type} {{", self.struct_name));

            if self.types.is_empty() {
                self.write_string(format!("    fn from_gil(_: Python, _: &Py<{}>) -> Self {{", self.struct_name));
                self.write_str("        Self::default()");
            } else {
                self.write_string(format!(
                    "    fn from_gil(py: Python, py_type: &Py<{}>) -> Self {{",
                    self.struct_name
                ));

                if impl_type.contains("Box<") {
                    self.write_string(format!(
                        "        Self::new(flat::{}::from_gil(py, py_type))",
                        self.struct_t_name
                    ));
                } else {
                    self.write_str("        Self::from_gil(py, &*py_type.borrow(py))");
                }
            }

            self.write_str("    }");
            self.write_str("}");
            self.write_str("");
        }
    }

    fn generate_new_method(&mut self) {
        match self.bind_type {
            PythonBindType::Enum => self.generate_enum_new_method(),
            PythonBindType::Struct => self.generate_struct_new_method(),
            PythonBindType::Union => self.generate_union_new_method(),
        }
    }

    fn generate_union_new_method(&mut self) {
        assert!(u8::try_from(self.types.len()).is_ok());

        self.write_str("    #[new]");
        self.write_str("    #[pyo3(signature = (item = None))]");
        self.write_string(format!("    pub fn new(item: Option<{}Union>) -> Self {{", self.struct_name));
        self.write_str("        Self { item }");
        self.write_str("    }");
        self.write_str("");
        self.write_str("    #[getter(item)]");
        self.write_str("    pub fn get(&self, py: Python) -> Option<PyObject> {");
        self.write_str("        match self.item.as_ref() {");

        for variable_info in &self.types {
            let variable_name = &variable_info[0];

            if variable_name == "NONE" {
                self.file_contents.push(Cow::Borrowed("            None => None,"));
            } else {
                self.file_contents.push(Cow::Owned(format!(
                    "            Some({}Union::{variable_name}(item)) => Some(item.to_object(py)),",
                    self.struct_name
                )));
            }
        }

        self.write_str("        }");
        self.write_str("    }");
    }

    fn generate_enum_new_method(&mut self) {
        self.write_str("    #[new]");
        assert!(u8::try_from(self.types.len()).is_ok());

        self.write_str("    #[pyo3(signature = (value=Default::default()))]");
        self.write_str("    pub fn new(value: u8) -> PyResult<Self> {");
        self.write_str("        match value {");

        for variable_info in &self.types {
            let variable_name = &variable_info[0];
            let variable_value = &variable_info[1];

            self.file_contents.push(Cow::Owned(format!(
                "            {variable_value} => Ok(Self::{variable_name}),"
            )));
        }

        if self.types.len() != usize::from(u8::MAX) {
            self.write_str("            v => Err(PyValueError::new_err(format!(\"Unknown value of {v}\"))),");
        }

        self.write_str("        }");
        self.write_str("    }");
    }

    fn generate_struct_new_method(&mut self) {
        self.write_str("    #[new]");
        self.write_str("    #[allow(clippy::too_many_arguments)]");

        if self.types.is_empty() {
            self.write_str("    pub fn new() -> Self {");
            self.write_str("        Self::default()");
            self.write_str("    }");
            return;
        }

        let mut signature_parts = Vec::new();
        let mut needs_python = false;

        for variable_info in &self.types {
            let variable_name = &variable_info[0];
            let variable_type = &variable_info[1];

            if variable_type.is_empty() {
                continue;
            }

            if variable_type.starts_with("Option<") {
                let inner_type = variable_type
                    .trim_start_matches("Option<")
                    .trim_start_matches("Box<")
                    .trim_end_matches('>');

                if Self::SPECIAL_BASE_TYPES.contains(&inner_type) {
                    needs_python = true;
                }

                signature_parts.push(format!("{variable_name}=None"));
            } else if !Self::BASE_TYPES.contains(&variable_type.as_str())
                && (variable_type.starts_with("Box<") || variable_type.ends_with('T'))
            {
                signature_parts.push(format!("{variable_name}=crate::get_py_default()"));
            } else if variable_type == "Vec<u8>" {
                signature_parts.push(format!("{variable_name}=crate::get_empty_pybytes()"));
            } else {
                signature_parts.push(format!("{variable_name}=Default::default()"));
            }
        }

        self.write_string(format!("    #[pyo3(signature = ({}))]", signature_parts.join(", ")));
        self.write_str("    pub fn new(");

        if needs_python {
            self.write_str("        py: Python,");
        }

        for variable_info in &self.types {
            let variable_name = &variable_info[0];
            let mut variable_type = variable_info[1].to_string();

            if variable_type.starts_with("Vec<") && variable_type.ends_with("T>") {
                variable_type = format!(
                    "Vec<Py<super::{}>>",
                    variable_type.trim_start_matches("Vec<").trim_end_matches("T>")
                );
            } else if variable_type == "Vec<u8>" {
                variable_type = String::from("Py<PyBytes>");
            } else if variable_type.starts_with("Box<") && variable_type.ends_with('>') {
                variable_type = format!(
                    "Py<super::{}>",
                    variable_type
                        .trim_start_matches("Box<")
                        .trim_end_matches('>')
                        .trim_end_matches('T')
                );
            } else if variable_type.starts_with("Option<") && variable_type.ends_with('>') {
                let inner_type = variable_type
                    .trim_start_matches("Option<")
                    .trim_start_matches("Box<")
                    .trim_end_matches('>')
                    .trim_end_matches('T');

                if Self::BASE_TYPES.contains(&inner_type) {
                    variable_type = format!("Option<{inner_type}>");
                } else if inner_type == "Float" {
                    variable_type = String::from("Option<crate::Floats>");
                } else if inner_type == "Bool" {
                    variable_type = String::from("Option<crate::Bools>");
                } else {
                    variable_type = format!("Option<Py<super::{inner_type}>>");
                }
            } else if !Self::BASE_TYPES.contains(&variable_type.as_str()) {
                if variable_type.ends_with('T') {
                    variable_type = format!("Py<super::{}>", variable_type.trim_end_matches('T'));
                } else {
                    variable_type = format!("super::{variable_type}");
                }
            }

            self.file_contents
                .push(Cow::Owned(format!("        {variable_name}: {variable_type},")));
        }

        self.write_str("    ) -> Self {");
        self.write_str("        Self {");

        for variable_info in &self.types {
            let variable_name = &variable_info[0];
            let variable_type = variable_info[1]
                .trim_start_matches("Option<")
                .trim_start_matches("Box<")
                .trim_end_matches('>');

            if Self::SPECIAL_BASE_TYPES.contains(&variable_type) {
                self.file_contents.push(Cow::Owned(format!(
                    "            {variable_name}: {variable_name}.map(|x| x.into_gil(py)),"
                )));
            } else {
                self.file_contents.push(Cow::Owned(format!("            {variable_name},")));
            }
        }

        self.write_str("        }");
        self.write_str("    }");
    }

    fn generate_str_method(&mut self) {
        self.write_str("    pub fn __str__(&self) -> String {");
        self.write_str("        format!(\"{self:?}\")");
        self.write_str("    }");
    }

    fn generate_repr_method(&mut self) {
        match self.bind_type {
            PythonBindType::Enum => self.generate_enum_repr_method(),
            PythonBindType::Struct => self.generate_struct_repr_method(),
            PythonBindType::Union => self.generate_union_repr_method(),
        }
    }

    fn generate_union_repr_method(&mut self) {
        self.write_str("    pub fn __repr__(&self, py: Python) -> String {");
        self.write_str("        match self.item.as_ref() {");

        for variable_info in &self.types {
            let variable_name = &variable_info[0];
            let variable_type = &variable_info[1];

            if variable_type.is_empty() {
                self.file_contents.push(Cow::Owned(format!(
                    "            None => String::from(\"{}()\"),",
                    self.struct_name
                )));
            } else {
                self.file_contents.push(Cow::Owned(format!(
                    "            Some({}Union::{variable_name}(item)) => format!(\"{}({{}})\", item.borrow(py).__repr__(py)),",
                    self.struct_name, self.struct_name
                )));
            }
        }

        self.write_str("        }");
        self.write_str("    }");
    }

    fn generate_enum_repr_method(&mut self) {
        self.write_str("    pub fn __repr__(&self) -> String {");
        self.write_string(format!("        format!(\"{}(value={{}})\", *self as u8)", self.struct_name));
        self.write_str("    }");
    }

    fn generate_struct_repr_method(&mut self) {
        if self.types.is_empty() {
            self.write_str("    pub fn __repr__(&self, _py: Python) -> String {");
            self.write_string(format!("        String::from(\"{}()\")", self.struct_name));
            self.write_str("    }");
            return;
        }

        self.write_str("    #[allow(unused_variables)]");
        self.write_str("    pub fn __repr__(&self, py: Python) -> String {");
        self.write_str("        format!(");

        let repr_signature = self
            .types
            .iter()
            .map(|variable_info| {
                let variable_name = &variable_info[0];
                let variable_type = variable_info[1].as_str();

                if variable_type == "String" {
                    format!("{variable_name}={{:?}}")
                } else if variable_type == "Vec<u8>" {
                    format!("{variable_name}=bytes([{{}}])")
                } else if variable_type.starts_with("Vec<") {
                    format!("{variable_name}=[{{}}]")
                } else {
                    format!("{variable_name}={{}}")
                }
            })
            .collect::<Vec<_>>()
            .join(", ");
        self.write_string(format!("            \"{}({repr_signature})\",", self.struct_name));

        for variable_info in &self.types {
            let variable_name = &variable_info[0];
            let variable_type = variable_info[1].as_str();

            if variable_type == "bool" {
                self.file_contents
                    .push(Cow::Owned(format!("            crate::bool_to_str(self.{variable_name}),")));
            } else if Self::BASE_TYPES.contains(&variable_type) {
                self.file_contents
                    .push(Cow::Owned(format!("            self.{variable_name},")));
            } else if variable_type.starts_with("Option<") {
                self.file_contents
                    .push(Cow::Owned(format!("            self.{variable_name}")));
                self.file_contents.push(Cow::Borrowed("                .as_ref()"));
                if Self::BASE_TYPES.into_iter().any(|t| variable_type.contains(t)) {
                    self.file_contents
                        .push(Cow::Borrowed("                .map(|i| format!(\"{i:?}\"))"));
                } else {
                    self.file_contents
                        .push(Cow::Borrowed("                .map(|x| x.borrow(py).__repr__(py))"));
                }
                self.file_contents
                    .push(Cow::Borrowed("                .unwrap_or_else(crate::none_str),"));
            } else if variable_type.starts_with("Vec<") {
                self.file_contents
                    .push(Cow::Owned(format!("            self.{variable_name}")));
                if Self::BASE_TYPES.into_iter().any(|t| variable_type.contains(t)) {
                    self.file_contents.push(Cow::Borrowed("                .as_bytes(py)"));
                    self.file_contents.push(Cow::Borrowed("                .iter()"));
                    self.file_contents
                        .push(Cow::Borrowed("                .map(ToString::to_string)"));
                } else {
                    self.file_contents.push(Cow::Borrowed("                .iter()"));
                    self.file_contents
                        .push(Cow::Borrowed("                .map(|x| x.borrow(py).__repr__(py))"));
                }
                self.file_contents
                    .push(Cow::Borrowed("                .collect::<Vec<String>>()"));
                self.file_contents.push(Cow::Borrowed("                .join(\", \"),"));
            } else if variable_type.ends_with('T') || variable_type.starts_with("Box<") {
                self.file_contents.push(Cow::Owned(format!(
                    "            self.{variable_name}.borrow(py).__repr__(py),"
                )));
            } else {
                self.file_contents
                    .push(Cow::Owned(format!("            self.{variable_name}.__repr__(),")));
            }
        }

        self.write_str("        )");
        self.write_str("    }");
    }

    fn generate_pack_method(&mut self) {
        self.write_str("    fn pack<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {");

        let name = if self.bind_type == PythonBindType::Enum {
            &self.struct_name
        } else {
            &self.struct_t_name
        };

        if self.bind_type == PythonBindType::Enum {
            self.write_string(format!("        let flat_t = flat::{name}::from(self);"));
        } else {
            self.write_string(format!("        let flat_t = flat::{name}::from_gil(py, self);"));
        }

        if self.has_complex_pack {
            self.write_str("        let size = flat_t.get_size().next_power_of_two();");
            self.write_str("");
            self.write_str("        let mut builder = FlatBufferBuilder::with_capacity(size);");
            self.write_str("        let offset = flat_t.pack(&mut builder);");
            self.write_str("        builder.finish(offset, None);");
            self.write_str("");
            self.write_str("        PyBytes::new_bound(py, builder.finished_data())");
        } else if self.bind_type == PythonBindType::Enum {
            self.write_str("        PyBytes::new_bound(py, &[flat_t.0])");
        } else {
            self.write_str("        let item = flat_t.pack();");
            self.write_str("");
            self.write_str("        PyBytes::new_bound(py, &item.0)");
        }

        self.write_str("    }");
    }

    fn generate_unpack_method(&mut self) {
        self.write_str("    #[staticmethod]");

        if self.bind_type == PythonBindType::Enum {
            self.write_str("    fn unpack(data: &[u8]) -> PyResult<Self> {");
            self.write_string(format!("        match root::<flat::{}>(data) {{", self.struct_name));
            self.write_str("            Ok(flat_t) => Ok(flat_t.into()),");
            self.write_str("            Err(e) => Err(flat_err_to_py(e)),");
            self.write_str("        }");
        } else {
            self.write_str("    fn unpack(py: Python, data: &[u8]) -> PyResult<Py<Self>> {");
            self.write_string(format!("        match root::<flat::{}>(data) {{", self.struct_name));
            self.write_str("            Ok(flat_t) => Ok(flat_t.unpack().into_gil(py)),");
            self.write_str("            Err(e) => Err(flat_err_to_py(e)),");
            self.write_str("        }");
        }

        self.write_str("    }");
    }

    fn generate_enum_hash_method(&mut self) {
        self.write_str("    pub fn __hash__(&self) -> u64 {");
        self.write_str("        crate::hash_u8(*self as u8)");
        self.write_str("    }");
    }

    fn generate_py_methods(&mut self) {
        self.write_str("#[pymethods]");
        self.write_string(format!("impl {} {{", self.struct_name));

        self.generate_new_method();
        self.write_str("");
        self.generate_str_method();
        self.write_str("");
        self.generate_repr_method();

        if self.bind_type == PythonBindType::Enum {
            self.write_str("");
            self.generate_enum_hash_method();
        }

        if self.bind_type != PythonBindType::Union {
            self.write_str("");
            self.generate_pack_method();
            self.write_str("");
            self.generate_unpack_method();
        }

        self.write_str("}");
        self.write_str("");
    }

    fn finish(self) -> io::Result<(String, String, Vec<Vec<String>>)> {
        let file_path = format!("{PYTHON_OUT_FOLDER}/{}.rs", self.filename);
        let file = Path::new(&file_path);

        fs::create_dir_all(file.parent().unwrap())?;
        fs::write(file, self.file_contents.join("\n"))?;

        Ok((self.filename, self.struct_name, self.types))
    }
}

fn camel_to_snake_case(variable_name: &str) -> String {
    let mut snake_case_parts: Vec<String> = Vec::new();

    let mut last_was_uppercase = false;
    for c in variable_name.chars() {
        if c.is_uppercase() {
            if last_was_uppercase {
                snake_case_parts.last_mut().unwrap().push(c.to_lowercase().next().unwrap());
            } else {
                snake_case_parts.push(c.to_lowercase().to_string());
            }

            last_was_uppercase = true;
        } else if c.is_ascii_digit() {
            snake_case_parts.push(c.to_lowercase().to_string());
            last_was_uppercase = false;
        } else {
            snake_case_parts.last_mut().unwrap().push(c);
            last_was_uppercase = false;
        }
    }

    snake_case_parts.join("_")
}

fn mod_rs_generator(type_data: &[(String, String, Vec<Vec<String>>)]) -> io::Result<()> {
    let mut file_contents = Vec::new();

    for (filename, _, _) in type_data {
        file_contents.push(Cow::Owned(format!("mod {filename};")));
        file_contents.push(Cow::Owned(format!("pub use {filename}::*;")));
    }

    file_contents.push(Cow::Borrowed(""));

    fs::write(format!("{PYTHON_OUT_FOLDER}/mod.rs"), file_contents.join("\n"))?;

    Ok(())
}

fn class_names_txt_generator(type_data: &[(String, String, Vec<Vec<String>>)]) -> io::Result<()> {
    let mut class_names = type_data
        .iter()
        .map(|(_, type_name, _)| format!("    {type_name}"))
        .collect::<Vec<_>>();
    class_names.sort();

    let file_contents = format!("[\n{}\n]", class_names.join(",\n"));

    fs::write("classes.txt", file_contents)?;

    Ok(())
}

fn pyi_generator(type_data: &[(String, String, Vec<Vec<String>>)]) -> io::Result<()> {
    let mut file_contents = vec![
        Cow::Borrowed("from __future__ import annotations"),
        Cow::Borrowed(""),
        Cow::Borrowed("from typing import Optional, Sequence"),
        Cow::Borrowed(""),
        Cow::Borrowed("__doc__: str"),
        Cow::Borrowed("__version__: str"),
        Cow::Borrowed(""),
        Cow::Borrowed("class InvalidFlatbuffer(ValueError): ..."),
        Cow::Borrowed(""),
    ];

    let primitive_map = [
        ("bool", "bool"),
        ("i32", "int"),
        ("u32", "int"),
        ("f32", "float"),
        ("String", "str"),
        ("u8", "int"),
        ("Vec<u8>", "bytes"),
    ];

    for (_, type_name, types) in type_data {
        let is_enum = !types.is_empty()
            && types
                .iter()
                .enumerate()
                .all(|(i, variable_info)| variable_info[1] == i.to_string());

        let is_union = !types.is_empty() && types[0][1].is_empty();

        file_contents.push(Cow::Owned(format!("class {type_name}:")));

        if is_union {
            let types = types
                .iter()
                .map(|variable_info| variable_info[0].as_str())
                .filter(|variable_name| *variable_name != "NONE")
                .collect::<Vec<_>>();
            let union_str = types.join(" | ");

            file_contents.push(Cow::Owned(format!("    item: Optional[{union_str}]")));
            file_contents.push(Cow::Borrowed(""));
            file_contents.push(Cow::Borrowed("    def __init__("));
            file_contents.push(Cow::Owned(format!("        self, item: Optional[{union_str}] = None")));
            file_contents.push(Cow::Borrowed("    ): ..."));
        } else {
            let mut python_types = Vec::new();

            'outer: for variable_info in types {
                let mut variable_name = variable_info[0].as_str();

                if variable_name == "NONE" {
                    continue;
                }

                if is_union {
                    variable_name = &variable_info[2];
                }

                let variable_type = if is_union {
                    format!("Option<{}>", variable_info[1])
                } else {
                    variable_info[1].clone()
                };

                if is_enum {
                    file_contents.push(Cow::Owned(format!("    {variable_name} = {type_name}({variable_type})")));
                    continue;
                }

                for (rust_type, python_type) in primitive_map {
                    if variable_type == rust_type {
                        python_types.push(python_type.to_string());
                        file_contents.push(Cow::Owned(format!("    {variable_name}: {python_type}")));
                        continue 'outer;
                    }
                }

                if variable_type.starts_with("Vec<") {
                    let type_name = variable_type
                        .trim_start_matches("Vec<")
                        .trim_end_matches('>')
                        .trim_end_matches('T');

                    python_types.push(format!("Sequence[{type_name}]"));
                    file_contents.push(Cow::Owned(format!("    {variable_name}: Sequence[{type_name}]")));
                } else if variable_type.starts_with("Option<") {
                    let type_name = variable_type
                        .trim_start_matches("Option<")
                        .trim_start_matches("Box<")
                        .trim_end_matches('>')
                        .trim_end_matches('T');

                    let python_type = if type_name == "bool" {
                        "bool"
                    } else if type_name == "i32" || type_name == "u32" {
                        "int"
                    } else if type_name == "f32" {
                        "float"
                    } else if type_name == "String" {
                        "str"
                    } else if type_name == "Float" {
                        "Float | float"
                    } else if type_name == "Bool" {
                        "Bool | bool"
                    } else {
                        type_name
                    };

                    python_types.push(format!("Optional[{python_type}]"));
                    file_contents.push(Cow::Owned(format!("    {variable_name}: Optional[{python_type}]")));
                } else if variable_type.starts_with("Box<") && variable_type.ends_with("T>") {
                    let type_name = variable_type.trim_start_matches("Box<").trim_end_matches("T>");

                    python_types.push(type_name.to_string());
                    file_contents.push(Cow::Owned(format!("    {variable_name}: {type_name}")));
                } else if variable_type.ends_with('T') {
                    let type_name = variable_type.trim_end_matches('T');

                    python_types.push(type_name.to_string());
                    file_contents.push(Cow::Owned(format!("    {variable_name}: {type_name}")));
                } else {
                    python_types.push(variable_type.clone());
                    file_contents.push(Cow::Owned(format!("    {variable_name}: {variable_type}")));
                }
            }

            if types.is_empty() {
                file_contents.push(Cow::Borrowed("    def __init__(self): ..."));
            } else if is_enum {
                file_contents.push(Cow::Borrowed(""));
                file_contents.push(Cow::Borrowed("    def __init__(self, value: int = 0):"));
                file_contents.push(Cow::Borrowed("        \"\"\""));
                file_contents.push(Cow::Borrowed(
                    "        :raises ValueError: If the `value` is not a valid enum value",
                ));
                file_contents.push(Cow::Borrowed("        \"\"\"\n"));
            } else {
                file_contents.push(Cow::Borrowed(""));
                file_contents.push(Cow::Borrowed("    def __init__("));
                file_contents.push(Cow::Borrowed("        self,"));

                let mut i = 0;
                for variable_info in types {
                    if &variable_info[0] == "NONE" {
                        continue;
                    }

                    let variable_name = &variable_info[0];

                    let variable_type = variable_info[1].clone();

                    let default_value = match variable_type.as_str() {
                        "bool" => Cow::Borrowed("False"),
                        "i32" | "u32" | "f32" | "u8" => Cow::Borrowed("0"),
                        "String" => Cow::Borrowed("\"\""),
                        "Vec<u8>" => Cow::Borrowed("b\"\""),
                        t => {
                            if t.starts_with("Vec<") {
                                Cow::Borrowed("[]")
                            } else if t.starts_with("Box<") {
                                let inner_type = t.trim_start_matches("Box<").trim_end_matches('>').trim_end_matches('T');
                                Cow::Owned(format!("{inner_type}()"))
                            } else if t.starts_with("Option<") {
                                Cow::Borrowed("None")
                            } else {
                                Cow::Owned(format!("{}()", t.trim_end_matches('T')))
                            }
                        }
                    };

                    let python_type = &python_types[i];
                    file_contents.push(Cow::Owned(format!(
                        "        {variable_name}: {python_type} = {default_value},"
                    )));

                    i += 1;
                }

                file_contents.push(Cow::Borrowed("    ): ..."));
            }
        }

        file_contents.push(Cow::Borrowed("    def __str__(self) -> str: ..."));
        file_contents.push(Cow::Borrowed("    def __repr__(self) -> str: ..."));
        file_contents.push(Cow::Borrowed("    def __hash__(self) -> str: ..."));

        if is_enum {
            file_contents.push(Cow::Borrowed("    def __int__(self) -> int: ..."));
            file_contents.push(Cow::Owned(format!(
                "    def __richcmp__(self, other: {type_name}, op: int) -> bool: ..."
            )));
        }

        if !is_union {
            file_contents.push(Cow::Borrowed("    def pack(self) -> bytes: ..."));
            file_contents.push(Cow::Borrowed("    @staticmethod"));
            file_contents.push(Cow::Owned(format!("    def unpack(data: bytes) -> {type_name}:")));
            file_contents.push(Cow::Borrowed("        \"\"\""));
            file_contents.push(Cow::Borrowed(
                "        :raises InvalidFlatbuffer: If the `data` is invalid for this type",
            ));
            file_contents.push(Cow::Borrowed("        \"\"\""));
        }

        file_contents.push(Cow::Borrowed(""));
    }

    fs::write("rlbot_flatbuffers.pyi", file_contents.join("\n"))?;

    Ok(())
}

fn main() -> io::Result<()> {
    println!("cargo:rerun-if-changed=flatbuffers-schema/comms.fbs");
    println!("cargo:rerun-if-changed=flatbuffers-schema/event.fbs");
    println!("cargo:rerun-if-changed=flatbuffers-schema/gamestate.fbs");
    println!("cargo:rerun-if-changed=flatbuffers-schema/matchstart.fbs");
    println!("cargo:rerun-if-changed=flatbuffers-schema/rendering.fbs");
    println!("cargo:rerun-if-changed=flatbuffers-schema/rlbot.fbs");

    set_current_dir(env!("CARGO_MANIFEST_DIR"))?;

    let mut schema_folder = Path::new(SCHEMA_FOLDER);
    if !schema_folder.exists() {
        schema_folder = Path::new(SCHEMA_FOLDER_BACKUP);
        assert!(schema_folder.exists(), "Could not find flatbuffers schema folder");
    }

    let schema_folder_str = schema_folder.display();

    Command::new(format!("{schema_folder_str}/{FLATC_BINARY}"))
        .args([
            "--rust",
            "--gen-object-api",
            "--gen-all",
            "--filename-suffix",
            "",
            "--rust-module-root-file",
            "-o",
            OUT_FOLDER,
            &format!("{schema_folder_str}/rlbot.fbs"),
        ])
        .spawn()?
        .wait()?;

    let out_folder = Path::new(OUT_FOLDER).join("rlbot").join("flat");

    assert!(
        out_folder.exists(),
        "Could not find generated folder: {}",
        out_folder.display()
    );

    // ^ the above generates the Rust flatbuffers code,
    // and the below we generates the wanted additional Python binds

    // read the current contents of the generated folder
    let generated_files = fs::read_dir(out_folder)?
        .map(|res| res.map(|e| e.path()))
        .collect::<Result<Vec<_>, io::Error>>()?;

    let mut type_data = Vec::new();

    for path in generated_files {
        let Some(mut python_bind_generator) = PythonBindGenerator::new(&path) else {
            continue;
        };

        python_bind_generator.add_get_size_derive(&path);
        python_bind_generator.generate_definition();
        python_bind_generator.generate_from_flat_impls();
        python_bind_generator.generate_to_flat_impls();
        python_bind_generator.generate_py_methods();

        type_data.push(python_bind_generator.finish()?);
    }

    mod_rs_generator(&type_data)?;
    pyi_generator(&type_data)?;
    class_names_txt_generator(&type_data)?;

    Ok(())
}
