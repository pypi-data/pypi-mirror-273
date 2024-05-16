# Cargo Workspace

Parse Rust Workspace files from a `Cargo.toml` file.

## Example

```python
from cargo_workspace import Workspace

# Path can be a file or directory:
workspace = Workspace.from_path('Cargo.toml')

for crate in workspace.crates:
	print(f'crate at {crate.path} has name {crate.name}')
```

Note that this crate uses getter functions instead of the conventional 

### Metadata

The metadata of each crate is accessible like so:

```python
meta = crate.workspace.get('some.custom.key')

if meta not None:
	print(f'custom metadata found: {meta}')
```
