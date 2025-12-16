# Fork Analysis Report for DunbrackLab/IPSAE

Repository: [DunbrackLab/IPSAE](https://github.com/DunbrackLab/IPSAE)


Description: Scoring function for interprotein interactions in AlphaFold2 and AlphaFold3


Stars: 171

Generated: 2025-12-16 13:21:39 UTC

Model: deepseek/deepseek-v3.2

## Fork Analysis

Found 10 active forks with significant changes.


### [y1zhou/IPSAE](https://github.com/y1zhou/IPSAE)

**Stats:**
- Commits ahead: 42
- Commits behind: 0
- Stars: 0

- Pull Requests:

  - [PR #1](https://github.com/DunbrackLab/IPSAE/pull/22)


- Last updated: 2025-12-09T04:13:03+00:00

**Summary of Changes:**
Based on the provided commits and diff, here is a summary of the changes introduced in the fork:

## Summary of Changes

This fork significantly refactors and enhances the original ipSAE scoring script, transforming it from a monolithic script into a modular, well-structured Python package with new functionality and improved robustness.

### Main Themes and Purposes

1. **Code Modernization and Refactoring**: The primary goal was to transform a single-file script (`ipsae.py`) into a proper Python package with clear separation of concerns, using dataclasses, enums, and type hints for better maintainability.

2. **Enhanced Functionality**: Added support for calculating scores between user-defined chain groups, allowing more flexible analysis of protein complexes.

3. **Improved Robustness**: Added extensive input validation, error handling, and safeguards to prevent misparsing of files and incorrect calculations.

### Key Innovations and Features

1. **New Chain Groups Feature**:
   - Added `--chain-groups` CLI argument to calculate scores between specified chain groups
   - Supports complex group definitions like `A/H+L` (chain A vs chains H+L treated as one group)
   - Includes ellipsis token (`...`) to include all default individual chain permutations
   - Proper handling of multi-chain groups in PyMOL script generation

2. **Comprehensive Refactoring**:
   - Converted to proper Python package structure under `src/ipsae/`
   - Introduced dataclasses (`Residue`, `StructureData`, `PAEData`, `ChainPairScoreResults`, `PerResScoreResults`, `ScoreResults`)
   - Created `InputModelType` enum for supported model types (AF2, AF3, Boltz1, Boltz2)
   - Modularized functionality into distinct functions with clear responsibilities

3. **Enhanced Input Handling**:
   - Added `-t/--model-type` flag to explicitly specify model type and skip auto-detection
   - Implemented comprehensive file parsing safeguards
   - Added validation for chain group definitions to prevent overlapping chains

4. **Improved Testing Infrastructure**:
   - Added integration tests comparing output against sample files
   - Created comprehensive test suite for chain group functionality
   - Added helper scripts for comparing differences to original script

5. **Performance Optimizations**:
   - Vectorized calculations using NumPy for better performance
   - Merged pDockQ and pDockQ2 functions to avoid recomputing masks
   - Optimized distance matrix calculations

### Architectural Changes

1. **Package Structure**:
   - Moved from single script to `src/ipsae/ipsae.py` with proper `__init__.py`
   - Added `pyproject.toml` for packaging
   - Made script runnable both as standalone and as installed package

2. **Data Flow**:
   - Clear separation between data loading (`load_structure`, `load_pae_data`)
   - Core calculation engine (`calculate_scores`) with well-documented algorithms
   - Output generation (`write_outputs`, `aggregate_byres_scores`) separate from calculations

3. **Error Handling**:
   - Added comprehensive validation for chain group definitions
   - Safeguards against misparsing different model types
   - Proper handling of missing or malformed input files

### Potential Impact and Value

1. **Developer Experience**: The modular structure makes it easier to extend, test, and maintain the codebase. Type hints and documentation improve code comprehension.

2. **Scientific Utility**: The chain groups feature enables more sophisticated analysis of protein complexes, particularly useful for studying multi-subunit interactions.

3. **Reliability**: Input validation and error handling reduce the risk of incorrect calculations due to misparsed files or user errors.

4. **Performance**: Vectorized operations and optimized algorithms improve calculation speed for large structures.

5. **Integration**: The package structure facilitates integration into larger bioinformatics pipelines and tools.

**Tags**: feature, functionality, improvement, refactor, test, documentation, bugfix, ui, installation

The fork represents a substantial improvement over the original script, transforming it from a research tool into a production-ready library while adding valuable new functionality for analyzing complex protein interactions.

**Commits:**

- [833619bb](/commit/833619bb6ccbc649f94d515eb5b6e7722a45663e) - <span style="color:green">+4</span>/<span style="color:red">-0</span> (1 files): fix: raise error when input chain groups contain the same chain on both sides [y1zhou <zhou.zy.yi@gmail.com>]

- [bd81a7a7](/commit/bd81a7a7a99a1a64730fc0843147eddbd6108721) - <span style="color:green">+109</span>/<span style="color:red">-38</span> (1 files): fix: add safeguards on input model types to avoid misparsing files or missing inputs [y1zhou <zhou.zy.yi@gmail.com>]

- [969031b9](/commit/969031b92ec4c87ead45213d0e677b9f0c4561cb) - <span style="color:green">+1076</span>/<span style="color:red">-307</span> (4 files): Merge pull request #2 from y1zhou/copilot/add-cli-argument-chain-groups [Yi Zhou <17245097+y1zhou@users.noreply.github.com>]

- [a1326ae3](/commit/a1326ae31322bac0e18f371eaf2f5fe37ec2f540) - <span style="color:green">+149</span>/<span style="color:red">-272</span> (1 files): Refactor test_scoring.py to run ipsae once per input file set [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [0c51f6b8](/commit/0c51f6b8bd8ea7dbdf1f27e729602114c4f5e8e7) - <span style="color:green">+17</span>/<span style="color:red">-12</span> (1 files): Refactor: Extract normalize_whitespace function to module level [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [b39e4318](/commit/b39e4318024aeb81b4555766bfd42b053ff8945f) - <span style="color:green">+373</span>/<span style="color:red">-0</span> (1 files): Add test_scoring.py with integration tests comparing output against sample files [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [5526d87e](/commit/5526d87ef52dfdbdea112ba957471c1d4badc470) - <span style="color:green">+7</span>/<span style="color:red">-7</span> (1 files): style: add back the newlines separating chain pairs in the output [y1zhou <zhou.zy.yi@gmail.com>]

- [99f2168e](/commit/99f2168e889d7b8c1433971e4e47b7592409d6ce) - <span style="color:green">+132</span>/<span style="color:red">-129</span> (1 files): Group chain pair outputs together: asym A->B, B->A, then max, with blank line separator [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [efdb80b3](/commit/efdb80b3f02465b74c6721e9f56b6f7a2e4e4d26) - <span style="color:green">+96</span>/<span style="color:red">-66</span> (2 files): Fix value differences in output: correct ipTM_af max calc, max row naming, and byres ordering [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [4cf95980](/commit/4cf959801c9e35d96c1828161ac654c33d5dd8df) - <span style="color:green">+7</span>/<span style="color:red">-23</span> (1 files): refactor: remove unused functions and update variable names for clarity [y1zhou <zhou.zy.yi@gmail.com>]

- [0410ca9e](/commit/0410ca9e9edede237a487143144703838f517c98) - <span style="color:green">+8</span>/<span style="color:red">-12</span> (1 files): fix: modify output whitespace to be as close to the original as possible [y1zhou <zhou.zy.yi@gmail.com>]

- [669ee851](/commit/669ee8513d43e1a5b3ab70dfb2d4787336efce8a) - <span style="color:green">+41</span>/<span style="color:red">-78</span> (1 files): fix: adjust ordering of chain groups [y1zhou <zhou.zy.yi@gmail.com>]

- [f9c457f6](/commit/f9c457f694624b21f4fc0621e590dcd1e131dac8) - <span style="color:green">+249</span>/<span style="color:red">-178</span> (2 files): Address review feedback: np.isin, g1/g2 naming, PyMOL script, ellipsis token, -g flag [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [1dd06978](/commit/1dd069784f98f6e90bf3fd8a372a10210d553ab0) - <span style="color:green">+447</span>/<span style="color:red">-638</span> (2 files): Refactor chain group scoring to reuse existing functions [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [5b87ff3a](/commit/5b87ff3a8f99edba0ddc45cc4840c975c3c5489d) - <span style="color:green">+21</span>/<span style="color:red">-6</span> (2 files): Address code review feedback - improve warning messages and documentation [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [d09cb52b](/commit/d09cb52b0b0209366ff6989afecfb4d4e088546f) - <span style="color:green">+231</span>/<span style="color:red">-0</span> (2 files): Add tests for chain group functionality [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [c7949a2e](/commit/c7949a2ec767da783f47688db362c1803454eff9) - <span style="color:green">+413</span>/<span style="color:red">-1</span> (1 files): Add --chain-groups CLI argument for calculating scores between specified chain groups [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [5e4e1f15](/commit/5e4e1f15b37c46b8ef12ebb571df96c1b22e06a5) - <span style="color:green">+0</span>/<span style="color:red">-0</span> (0 files): Initial plan [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [7ae6525c](/commit/7ae6525c7c68f9a95a2763222cf985c4bc1cb2e9) - <span style="color:green">+57</span>/<span style="color:red">-41</span> (2 files): fix: better handling of file IO and remove unused code [y1zhou <zhou.zy.yi@gmail.com>]

- [157c7917](/commit/157c7917d13a6e16c1f07cd25d98274b72e41366) - <span style="color:green">+6</span>/<span style="color:red">-0</span> (1 files): docs(readme): add introduction to the installed script [y1zhou <zhou.zy.yi@gmail.com>]

- [723b5961](/commit/723b5961a11c76947d4def76cb9eeb52475ead9d) - <span style="color:green">+2007</span>/<span style="color:red">-1719</span> (6 files): build: runnable as a script, and useable as an installed package [y1zhou <zhou.zy.yi@gmail.com>]

- [37beeda7](/commit/37beeda78ed7174bb6e9cc7a9ba03e0cf45492e4) - <span style="color:green">+6</span>/<span style="color:red">-6</span> (1 files): refactor: make it easier to see chain-pair and pymol script output to stdout [y1zhou <zhou.zy.yi@gmail.com>]

- [9c8ff682](/commit/9c8ff6824887561f4048427e979ca085e1ccab72) - <span style="color:green">+63</span>/<span style="color:red">-62</span> (1 files): fix: store input cutoffs in the returned object; save integers when writing to files [y1zhou <zhou.zy.yi@gmail.com>]

- [443b43c1](/commit/443b43c1113275dc88a6fb520e9acc023bb47c2b) - <span style="color:green">+186</span>/<span style="color:red">-69</span> (1 files): Merge pull request #1 from y1zhou/copilot/refactor-summary-lines-dataclass [Yi Zhou <17245097+y1zhou@users.noreply.github.com>]

- [1e11f5a3](/commit/1e11f5a3e48826c189e5166a2c0f98196b15eba7) - <span style="color:green">+26</span>/<span style="color:red">-24</span> (1 files): Rename SummaryResult to ChainPairScoreResults and update field names [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [3b72ef12](/commit/3b72ef12df2ee1e079a913b2a9d61efcc5d43f2d) - <span style="color:green">+8</span>/<span style="color:red">-1</span> (1 files): Update aggregate_byres_scores docstring with return type details [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [256b52ea](/commit/256b52ea0655c242cd5a2a63038286ad2b57244e) - <span style="color:green">+169</span>/<span style="color:red">-61</span> (1 files): Refactor summary_lines to use SummaryResult dataclass [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [5b27a26a](/commit/5b27a26a29e29094a816d7fa6d989f3f1d138100) - <span style="color:green">+0</span>/<span style="color:red">-0</span> (0 files): Initial plan [copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>]

- [efbbc5ba](/commit/efbbc5ba213add54eb4a38d5a31e88f17a7ffe78) - <span style="color:green">+308</span>/<span style="color:red">-241</span> (1 files): refactor: moving around code chunks for better readability [y1zhou <zhou.zy.yi@gmail.com>]

- [6f8412b0](/commit/6f8412b02eb96938dcb8f0555852985337a3d485) - <span style="color:green">+99</span>/<span style="color:red">-25</span> (1 files): refactor: move per-residue line formatting to a separate dataclass [y1zhou <zhou.zy.yi@gmail.com>]

- [2f365de3](/commit/2f365de3172274bcf013356e7fe166c2d02163af) - <span style="color:green">+8372</span>/<span style="color:red">-22</span> (12 files): test: add example files because the original ones were missing iptm inputs [y1zhou <zhou.zy.yi@gmail.com>]

- [b3bdb678](/commit/b3bdb678cb7d4478e603b93fa36a30b9474081f1) - <span style="color:green">+30</span>/<span style="color:red">-21</span> (1 files): feat: add cli arg for forcing the input model type and skip guessing [y1zhou <zhou.zy.yi@gmail.com>]

- [39fffbc0](/commit/39fffbc06000c286534c58266db2b35f8d4f51e5) - <span style="color:green">+28</span>/<span style="color:red">-26</span> (1 files): feat: reach parity with the orignal script for all except row orders in the .pml output [y1zhou <zhou.zy.yi@gmail.com>]

- [392d1fbe](/commit/392d1fbe58685fb29e2184cd3f157b0f239b4413) - <span style="color:green">+78</span>/<span style="color:red">-78</span> (1 files): fix: WIP get per-residue scores calculated correctly [y1zhou <zhou.zy.yi@gmail.com>]

- [6f1ab177](/commit/6f1ab17711f3357c8b81a670c6a21c8de4d6d680) - <span style="color:green">+15</span>/<span style="color:red">-52</span> (1 files): perf: merge pDockQ and pDockQ2 functions to avoid recomputing masks [y1zhou <zhou.zy.yi@gmail.com>]

- [775a33ed](/commit/775a33edd049cae0b0a1f34ff296ddcaa6742a90) - <span style="color:green">+56</span>/<span style="color:red">-0</span> (1 files): test: helper script to compare differences to the original script [y1zhou <zhou.zy.yi@gmail.com>]

- [1d8142c8](/commit/1d8142c8ea0b667d9816c692d969f352da44c654) - <span style="color:green">+28</span>/<span style="color:red">-17</span> (1 files): fix(pdockq): fix bug where chain1 residue indices were not included in pDockQ calculations [y1zhou <zhou.zy.yi@gmail.com>]

- [3321ed92](/commit/3321ed9298f9ebc35594642d56b2840e79d401d0) - <span style="color:green">+120</span>/<span style="color:red">-62</span> (1 files): refactor: WIP of cleaning up the calculate_scores beast [y1zhou <zhou.zy.yi@gmail.com>]

- [649faaab](/commit/649faaabd68786c742dfc6d622b536021eccc1de) - <span style="color:green">+172</span>/<span style="color:red">-103</span> (1 files): feat: refactor the file IO section [y1zhou <zhou.zy.yi@gmail.com>]

- [c74d2c1b](/commit/c74d2c1b6869d31352cf7feb440cf25c1480c649) - <span style="color:green">+58</span>/<span style="color:red">-60</span> (1 files): refactor: clean up main function [y1zhou <zhou.zy.yi@gmail.com>]

- [c7000257](/commit/c7000257e59f352fccb942d959d961dd3e38ad4a) - <span style="color:green">+70</span>/<span style="color:red">-0</span> (1 files): ci: add pre-commit config [y1zhou <zhou.zy.yi@gmail.com>]

- [5e8061a7](/commit/5e8061a71cb428c3bc469c83e82502ae91da7786) - <span style="color:green">+1249</span>/<span style="color:red">-910</span> (1 files): refactor: WIP initial attempt to clean up the script with LLMs [y1zhou <zhou.zy.yi@gmail.com>]


---

### [ullahsamee/IPSAE](https://github.com/ullahsamee/IPSAE)

**Stats:**
- Commits ahead: 6
- Commits behind: 0
- Stars: 9

- Pull Requests:


- Last updated: 2025-09-15T22:07:36+00:00

**Summary of Changes:**
Based on the provided commits and diff, here is a summary of the changes introduced in this fork.

### Summary of Changes

The primary innovation in this fork is the **transformation of the IPSAE tool from a standalone Python script into a formal, installable Python package**. The changes focus on improving usability, distribution, and documentation.

**Main Themes and Purposes:**
1.  **Packaging and Distribution:** The core change is the creation of a `pip`-installable package (`ipsae`). This simplifies installation and makes the tool accessible via the Python Package Index (PyPI).
2.  **Improved User Experience:** The command-line interface (CLI) has been formalized with a `--help` option and clearer usage examples, moving away from direct script execution.
3.  **Project Structure Refactoring:** The code has been reorganized into a standard Python package layout (`src/ipsae/`), separating core logic, CLI, and tests.
4.  **Documentation Overhaul:** The `README.md` has been completely rewritten to serve as comprehensive package documentation, including installation, usage, and output explanations.

**Significant New Features and Improvements:**
*   **New Package Structure:** The project now follows modern Python packaging conventions with `pyproject.toml`, `MANIFEST.in`, and a `src`-based layout.
*   **Entry Point CLI:** A new CLI (`ipsae/cli.py`) is created, allowing users to run the tool simply by typing `ipsae` in the terminal after installation.
*   **Enhanced Documentation:** The new README is more user-friendly, featuring an animated GIF, clear command examples for AlphaFold2, AlphaFold3, and Boltz1, and detailed descriptions of output files.

**Notable Code Refactoring:**
*   The original monolithic `ipsae.py` script was split into modular components (`core.py` for logic, `cli.py` for interface).
*   The script was temporarily deleted (`[60e8b29c](https://github.com/DunbrackLab/IPSAE/commit/60e8b29c)`) and then re-added (`[6849b16d](https://github.com/DunbrackLab/IPSAE/commit/6849b16d)`), likely to reconcile the old standalone script with the new package structure. The final state includes both the package and the original script.
*   Test files were added (`tests/`), indicating a move towards a more robust and testable codebase.

**Potential Impact and Value:**
*   **Lower Barrier to Entry:** Users can now install the tool with a single `pip` command instead of manually downloading scripts and managing dependencies.
*   **Easier Integration:** Being a package facilitates its use as a dependency in other bioinformatics pipelines or scripts.
*   **Professional Presentation:** The standardized structure and comprehensive documentation make the project more accessible and maintainable, encouraging wider adoption and collaboration.

### Tags
installation, feature, functionality, ui, refactor, documentation, test

**Commits:**

- [eba5e0b1](/commit/eba5e0b1ef1abddbdd98051987c6de4bad472288) - <span style="color:green">+2</span>/<span style="color:red">-2</span> (1 files): Merge branch 'main' of https://github.com/ullahsamee/IPSAE [Samee Ullah <sameeullah@bs.qau.edu.pk>]

- [79b9a1c8](/commit/79b9a1c8b61b45c392e6233f620390d12cf95b52) - <span style="color:green">+1</span>/<span style="color:red">-1</span> (1 files): Update README.md [Samee Ullah <sameeullah@bs.qau.edu.pk>]

- [d7d49273](/commit/d7d4927347f884488b8f06ba9808c0c3c9042f99) - <span style="color:green">+1</span>/<span style="color:red">-1</span> (1 files): Update README.md [Samee Ullah <sameeullah@bs.qau.edu.pk>]

- [6849b16d](/commit/6849b16de8f9a49013f2bc666af87ff1b75d5312) - <span style="color:green">+970</span>/<span style="color:red">-0</span> (2 files): missing dunbrack ipsae script uploaded back [Samee Ullah <sameeullah@bs.qau.edu.pk>]

- [1676a005](/commit/1676a0058b1cb5c2683fb81c9293b7e781911f42) - <span style="color:green">+1333</span>/<span style="color:red">-105</span> (21 files): ipsae pip package [Samee Ullah <sameeullah@bs.qau.edu.pk>]

- [60e8b29c](/commit/60e8b29c0f265e12fac91232d921b37523f0a054) - <span style="color:green">+0</span>/<span style="color:red">-970</span> (1 files): Delete ipsae.py [Samee Ullah <sameeullah@bs.qau.edu.pk>]


---

### [s-nitz/IPSAE](https://github.com/s-nitz/IPSAE)

**Stats:**
- Commits ahead: 5
- Commits behind: 0
- Stars: 0

- Pull Requests:


- Last updated: 2025-12-05T18:40:35+00:00

**Summary of Changes:**
## Summary of Changes

This fork introduces significant improvements to the **ipSAE** (inter-protein Statistical Aromatic Environment) calculation tool, with a primary focus on **performance optimization through vectorization** and enhanced **testing infrastructure**.

### Main Themes and Purposes
1. **Performance Optimization**: The core ipSAE calculation algorithm has been vectorized to improve computational efficiency
2. **Code Organization**: Major refactoring to create a proper Python package structure
3. **Testing Infrastructure**: Comprehensive test suite development with example data
4. **Example Documentation**: Added practical usage examples with real protein complex data

### Key Changes and Innovations

#### 1. Vectorized ipSAE Calculation
- The main algorithmic improvement involves vectorizing the ipSAE calculation
- Expected to provide significant performance gains for large protein complex analyses
- Changes concentrated in `ipsae.py` with substantial code modifications (1,067+ lines added/modified)

#### 2. Package Restructuring
- Created proper Python package structure with `src/` directory
- Separated CLI functionality into `src/cli.py`
- Added proper `__init__.py` files for package initialization
- Moved main functionality from standalone `ipsae.py` to package module

#### 3. Comprehensive Testing Suite
- Added extensive testing with `test/test_ipsae.py`
- Included real-world test data including AlphaFold2 multimer predictions (RAF1_KSR1_MEK1 complex)
- Added support for testing with zip file inputs (`test_2971.zip`)
- Created example output files for validation (.pml, .txt formats)

#### 4. Example Documentation
- Added `Example/` directory with complete workflow examples
- Includes both AlphaFold2 multimer and custom fold data
- Provides PyMOL visualization scripts (.pml) and result files
- Added `Readme.md` to explain example usage

#### 5. Git Configuration
- Added `.gitignore` to properly manage test directories and cache files
- Configured to include necessary test files while excluding generated outputs

### Potential Impact
- **Performance**: Vectorization should significantly speed up ipSAE calculations, especially for large protein complexes
- **Maintainability**: Package structure improves code organization and future development
- **Usability**: Comprehensive examples and tests make the tool more accessible to researchers
- **Reliability**: Robust testing ensures calculation accuracy across different input types

### Tags
- **feature** - Vectorized calculation represents a significant new capability
- **improvement** - Performance optimization through vectorization
- **refactor** - Major code reorganization into package structure
- **test** - Comprehensive testing infrastructure added
- **documentation** - Added practical examples and usage documentation
- **functionality** - Enhanced input handling (zip file support)

The changes transform ipSAE from a standalone script into a well-structured, performant Python package with professional-grade testing and documentation, positioning it for broader adoption in structural bioinformatics workflows.

**Commits:**

- [039c9d05](/commit/039c9d05e519031bdf86f13246844ffe79a4c77d) - <span style="color:green">+24556</span>/<span style="color:red">-24166</span> (31 files): Merge pull request #4 from s-nitz/vectorize [Sam Nitz <39832537+s-nitz@users.noreply.github.com>]

- [dacc26a0](/commit/dacc26a07126449f45cdde2fc007065d8af69a9d) - <span style="color:green">+321</span>/<span style="color:red">-300</span> (5 files): testing for zipfiles [Sam Nitz <snitz@rockefeller.edu>]

- [34b2f437](/commit/34b2f4376175f6c009b08110a275e51c7e18d2e6) - <span style="color:green">+24524</span>/<span style="color:red">-24405</span> (29 files): moved files, added testing [Sam Nitz <snitz@rockefeller.edu>]

- [7c97f4ef](/commit/7c97f4ef45f70a38b86e406b8ffaf5195cd944b5) - <span style="color:green">+16</span>/<span style="color:red">-0</span> (2 files): testing setup [Sam Nitz <snitz@rockefeller.edu>]

- [1b50144f](/commit/1b50144fa2960205399a01bcff1a845d96cc638e) - <span style="color:green">+1067</span>/<span style="color:red">-833</span> (1 files): all edits so far [Sam Nitz <snitz@rockefeller.edu>]


---

### [LevitateBio/IPSAE](https://github.com/LevitateBio/IPSAE)

**Stats:**
- Commits ahead: 5
- Commits behind: 3
- Stars: 0

- Pull Requests:


- Last updated: 2025-04-16T20:39:10+00:00

**Summary of Changes:**
### Summary of Changes

This fork introduces **Docker support and CI/CD automation** via Drone CI, focusing on containerization and automated version tagging. The changes are centered around improving deployment and build processes.

### Key Changes

1. **Added Docker Support** (`Dockerfile`):
   - Created a minimal Docker image based on Alpine Linux (3.19).
   - Sets up a working directory (`/IPSAE`) and copies the entire project into the container.
   - This enables portable, reproducible deployments.

2. **Implemented Automated Version Tagging** (`cut_version_tag.sh`):
   - Introduced a shell script that reads a `VERSION` file, creates a Git tag (`v<version>`), and pushes it to the repository.
   - Facilitates semantic versioning and release automation.

3. **Added CI/CD Pipeline** (`.drone.yml`):
   - Configured a Drone CI pipeline with two main steps:
     - **Docker Build**: Automatically builds a Docker image tagged with the commit SHA and pushes it to a registry.
     - **Version Tagging**: Triggers the `cut_version_tag.sh` script on pushes to the `main` branch, automating version releases.

4. **Added Version File** (`VERSION`):
   - Created a simple file to store the project version (initialized as `1.0.0`), serving as the source of truth for the tagging script.

### Themes and Purpose
- **Containerization**: Simplifies deployment by packaging the application into a lightweight Docker container.
- **Automation**: Automates Docker image builds and version tagging through CI/CD, reducing manual steps.
- **Release Management**: Implements a structured approach to versioning and tagging releases.

### Impact
- **Portability**: The Docker image allows consistent execution across different environments.
- **Efficiency**: Automated pipelines reduce manual overhead for building and releasing.
- **Traceability**: Version tagging improves release tracking and rollback capabilities.

### Tags
- installation
- feature
- ci

**Commits:**

- [85f18ec1](/commit/85f18ec10d82adad7a457925c9ede79319abea10) - <span style="color:green">+25</span>/<span style="color:red">-0</span> (2 files): Merge pull request #1 from LevitateBio/docker [Brandon Frenz <brandon.frenz@gmail.com>]

- [e8310af0](/commit/e8310af0f0cc8fc3ff5c3f9d808f09e19edc139a) - <span style="color:green">+17</span>/<span style="color:red">-0</span> (1 files): added cut version tag [Brandon Frenz <brandon.frenz@gmail.com>]

- [939412c7](/commit/939412c793ee68eb296b9e53b769343841a6b729) - <span style="color:green">+8</span>/<span style="color:red">-0</span> (1 files): added Dockerfile [Brandon Frenz <brandon.frenz@gmail.com>]

- [83b7b385](/commit/83b7b3856486a5dcd6f6990fe6e580356358c3b8) - <span style="color:green">+1</span>/<span style="color:red">-0</span> (1 files): added version [Brandon Frenz <brandon.frenz@gmail.com>]

- [be72196a](/commit/be72196a033c90c3752c461c103a604621f7e7a6) - <span style="color:green">+49</span>/<span style="color:red">-0</span> (1 files): added drone yaml [Brandon Frenz <brandon.frenz@gmail.com>]


---

### [hemeai/IPSAE](https://github.com/hemeai/IPSAE)

**Stats:**
- Commits ahead: 3
- Commits behind: 0
- Stars: 0

- Pull Requests:


- Last updated: 2025-12-12T12:50:46+00:00

**Summary of Changes:**
## Summary of Changes

The fork introduces a new Modal Labs wrapper script for running IPSAE (Interpretable Predicted Structural Alignment Error) calculations on cloud infrastructure. This is a significant addition that enables scalable, parallel processing of protein structure analysis.

### Main Themes and Purpose
- **Cloud-based IPSAE Processing**: Creates a Modal containerized workflow to run IPSAE calculations on AlphaFold2, AlphaFold3, and Boltzmann models
- **Automated Input Discovery**: Implements intelligent file discovery and pairing for different model types
- **Batch Processing Support**: Enables processing multiple structure/PAE file pairs with configurable limits

### Key Features and Improvements
1. **Modal Integration**: Wraps the DunbrackLab IPSAE CLI in a Modal container with GPU support
2. **Multi-Model Support**: Handles AlphaFold2, AlphaFold3, and Boltzmann model outputs with dedicated discovery logic
3. **Flexible Input Discovery**: Automatically pairs PAE files with corresponding structure files using naming patterns
4. **Output Organization**: Structures outputs by run identifier and model type for clear organization
5. **Performance Features**: Includes skip-existing functionality, processing limits, and configurable timeouts

### Architectural Changes
- **New Script File**: Creates `modal_ipsae.py` as a standalone Modal application
- **Job Management System**: Implements `IpsaeJob` dataclass to track processing units
- **Discovery Pipeline**: Separate functions for each model type (`_discover_af2_jobs`, `_discover_af3_jobs`, `_discover_boltz_jobs`)
- **Remote Execution**: `run_ipsae` Modal function handles containerized IPSAE execution

### Notable Implementation Details
- **GPU Configuration**: Supports A10G, A100, H100, and L4 GPUs via environment variables
- **File Handling**: Transfers files as bytes to/from Modal containers
- **Error Handling**: Comprehensive validation and error reporting for missing files
- **Deduplication**: Prevents duplicate processing of identical PAE/structure combinations

### Usage and Impact
The script enables users to run IPSAE calculations at scale using Modal's cloud infrastructure, significantly reducing local computational requirements. It's particularly valuable for researchers processing large batches of protein structure predictions from tools like AlphaFold and Boltzmann generators.

**Tags**: feature, functionality, improvement, refactor

**Commits:**

- [ee21d698](/commit/ee21d698ff6f777926da0b2dfe0930acba82dbbd) - <span style="color:green">+2</span>/<span style="color:red">-0</span> (1 files): Update modal_ipsae.py with usage instructions [Satish Gaurav <36672530+deepsatflow@users.noreply.github.com>]

- [801b13b8](/commit/801b13b891f2372de470d67b8332a600f236cb44) - <span style="color:green">+482</span>/<span style="color:red">-0</span> (1 files): Merge pull request #1 from hemeai/deepsatflow-patch-1 [Satish Gaurav <36672530+deepsatflow@users.noreply.github.com>]

- [ed2a4c05](/commit/ed2a4c055d71ec8df454172c0fa87003f5cde2a7) - <span style="color:green">+482</span>/<span style="color:red">-0</span> (1 files): Add Modal Script for IPSAE calculation [Satish Gaurav <36672530+deepsatflow@users.noreply.github.com>]


---

### [QVQuality/IPSAE](https://github.com/QVQuality/IPSAE)

**Stats:**
- Commits ahead: 2
- Commits behind: 0
- Stars: 0

- Pull Requests:


- Last updated: 2025-11-28T14:07:33+00:00

**Summary of Changes:**
## Summary of Changes

The fork introduces two key improvements to the `ipsae.py` script: a **custom output directory feature** and a **bug fix** for calculating `n0res` values in complexes with zero interface residues.

### 1. Custom Output Directory Feature
- **Purpose**: Allows users to specify a custom output directory for generated files instead of always writing to the same directory as the input PDB/CIF file.
- **Implementation**:
  - Added an optional `[<outdir>]` parameter to all usage patterns (AF2, AF3, Boltz1).
  - Modified file path handling using `pathlib.Path` for better cross‑platform compatibility.
  - Output files (`*.txt`, `*_byres.txt`, `*.pml`) are now written to the specified directory (defaults to current directory if not provided).
  - Updated help messages to clarify the new optional argument.

### 2. Bug Fix for `n0res` Calculation
- **Issue**: The calculation of `n0res` (number of residues in chain2 with PAE below cutoff for each residue in chain1) was incorrect when `ipsae_d0res_asym` equaled zero, leading to an undefined `max_index`.
- **Fix**: Added a check to set `max_index` to `None` when `interchain_values` (the array of per‑residue ipSAE values) is empty or all zeros, preventing an index‑out‑of‑bounds error.
  - This ensures `n0res[chain1][chain2]` and `d0res[chain1][chain2]` are only assigned when a valid maximum exists.

### 3. Code Quality Improvements
- **Refactoring**: 
  - Replaced `import sys, os, math` with separate imports for clarity.
  - Used `Path` objects for file operations.
  - Improved formatting and spacing (e.g., consistent spacing around operators, line breaks for long conditions).
- **Logic Enhancements**:
  - Fixed a bug in the `valid_pairs_matrix` calculation (now uses `np.outer` to correctly mask inter‑chain pairs).
  - Clarified variable names and added comments for better readability.

### 4. Impact
- **Usability**: Users can now organize output files flexibly, useful for batch processing or keeping results separate from inputs.
- **Robustness**: The bug fix prevents crashes when analyzing complexes with no inter‑chain contacts (PAE ≥ cutoff for all residue pairs).
- **Maintainability**: Cleaner code structure and better adherence to Python best practices.

### Tags
- `feature` – adds custom output directory support.
- `bugfix` – fixes `n0res` calculation for edge cases.
- `refactor` – improves code organization and readability.
- `ui` – updates command‑line interface documentation.

**Commits:**

- [73accb58](/commit/73accb58c34bb9db342ecb1a87a63bc38262ab00) - <span style="color:green">+2</span>/<span style="color:red">-2</span> (1 files): fix: correct n0res calculation for complexes with ipSAE=0 [Sotiris Niarchos <sot.niarchos@gmail.com>]

- [a70c2b18](/commit/a70c2b18508d68205cf75b6c402ec895f438b32c) - <span style="color:green">+407</span>/<span style="color:red">-373</span> (1 files): custom output path [Sotiris Niarchos <sot.niarchos@gmail.com>]


---

### [Barry0121/IPSAE](https://github.com/Barry0121/IPSAE)

**Stats:**
- Commits ahead: 2
- Commits behind: 0
- Stars: 0

- Pull Requests:


- Last updated: 2025-11-20T15:59:13+00:00

**Summary of Changes:**
### Summary of Changes

This fork introduces significant updates focused on protein-ligand complex analysis and structural biology workflows. The changes primarily enhance the functionality for handling protein-ligand docking predictions and improve the tool's capability to process complex molecular structures.

**Key Themes and Purposes:**
1. **Enhanced Protein-Ligand Complex Support**: The main innovation is expanding the `ipsae.py` script to accept protein-ligand complexes, enabling more comprehensive structural analysis workflows.
2. **Streamlined Configuration Management**: Introduction of structured configuration files and results organization for better reproducibility and data management.
3. **Cleanup and Maintenance**: Removal of unnecessary files and directories to maintain a clean codebase.

**Main Changes:**
- **Significant Feature Addition**: The `ipsae.py` script now supports protein-ligand complex analysis, with 6,312 lines of new code adding substantial functionality for molecular docking and structural predictions.
- **Configuration System Overhaul**: Multiple new configuration files (`config.yaml`, JSON configs, NPZ data files) provide structured handling of prediction parameters, constraints, and results.
- **Example Integration**: Added comprehensive examples including PyMOL scripts (`*.pml`) and text files demonstrating practical usage with specific protein-ligand complexes (AURKA_0_TPX2_0 model).
- **Results Organization**: Created a hierarchical results structure with separate directories for predictions, processed data, manifests, and molecular data files.

**Technical Improvements:**
- The changes introduce a robust pipeline for protein-ligand interaction analysis with support for multiple data formats (CIF, NPZ, JSON, PKL).
- Enhanced data serialization and configuration management through structured file organization.
- Maintenance cleanup removing 181 lines of unnecessary logging and configuration files.

**Impact:**
These changes significantly expand the tool's applicability in computational biology and drug discovery workflows, providing researchers with enhanced capabilities for analyzing protein-ligand interactions and structural predictions.

**Tags:** `feature`, `functionality`, `improvement`, `refactor`

**Commits:**

- [d6b0b33e](/commit/d6b0b33e56d68348d19f31c8c11253641d017472) - <span style="color:green">+0</span>/<span style="color:red">-181</span> (2 files): Delete protein_ligand_example/boltz_results_config/lightning_logs/version_0 directory [Barry Xue <xzexin0121@gmail.com>]

- [27a6c381](/commit/27a6c381d5c14a7e03beea7fa8424fa8a6f0853e) - <span style="color:green">+6312</span>/<span style="color:red">-23</span> (21 files): Update the ipsae script to accept protein-ligand complex & attach test example [Barry Xue <xzexin0121@gmail.com>]


---

### [gebauer/IPSAE](https://github.com/gebauer/IPSAE)

**Stats:**
- Commits ahead: 2
- Commits behind: 3
- Stars: 0

- Pull Requests:


- Last updated: 2025-03-31T13:00:38+00:00

**Summary of Changes:**
## Summary of Changes

This fork introduces a significant architectural transformation of the IPSAE project, converting it from a standalone script into a modular Python library. The changes represent a major restructuring effort that establishes a foundation for future development.

### Main Themes and Purposes:
- **Library modularization**: The core IPSAE functionality has been reorganized into a proper Python package structure with separate modules for core calculations, data models, and visualization
- **Project scaffolding**: Created comprehensive project infrastructure including package metadata, requirements, and testing structure
- **Future planning**: Added a detailed roadmap (ToDo.txt) outlining a 6-phase development plan

### Significant New Features and Improvements:
- **Package structure**: Created `library/ipsae/` with organized modules (`core/`, `models/`, `visualization/`)
- **Package distribution**: Added `setup.py` and package metadata files for proper Python packaging
- **Example integration**: Provided example scripts and test files demonstrating library usage
- **Documentation foundation**: Added README files and project planning documentation

### Notable Architectural Changes:
- **Modular design**: Separated concerns into distinct modules (calculator, parser, utils, data models)
- **Package-ready structure**: Implemented standard Python package layout with `__init__.py` files
- **Testing infrastructure**: Created test directory structure for future test development

### Potential Impact and Value:
- Enables the IPSAE tool to be installed via pip and used as a dependency in other projects
- Provides a scalable foundation for adding new features and visualization tools
- Makes the codebase more maintainable and testable through proper modularization
- Sets clear direction for future development through the comprehensive roadmap

## Tags
**installation, feature, refactor, documentation, test**

*Note: The first commit shows an unusually large number of insertions (4+ million lines), which likely includes binary files (PDB structures, JSON data) rather than just source code changes. The core architectural transformation is reflected in the package structure creation and modularization of the codebase.*

**Commits:**

- [6aeb02cc](/commit/6aeb02cc2d92d5909c594098079c71341bd46c00) - <span style="color:green">+359</span>/<span style="color:red">-0</span> (4 files): ipsae.py transfered to library (mostly by AI added coding) 2nd [Jan Gebauer <jan.gebauer@uni-koeln.de>]

- [9525df6b](/commit/9525df6b625d59c018a74e82afb0ea4503156c72) - <span style="color:green">+4023626</span>/<span style="color:red">-19332</span> (45 files): ipsae.py transfered to library (mostly by AI added coding) [Jan Gebauer <jan.gebauer@uni-koeln.de>]


---

### [cytokineking/IPSAE](https://github.com/cytokineking/IPSAE)

**Stats:**
- Commits ahead: 1
- Commits behind: 0
- Stars: 0

- Pull Requests:


- Last updated: 2025-11-27T03:16:42+00:00

**Summary of Changes:**
## Summary of Changes

This commit introduces a new batch processing script `summarize_ipsae.py` that extends the ipSAE (interface Predicted Aligned Error) analysis capability to support both AlphaFold3 and Boltz-2 protein structure prediction outputs.

### Main Themes and Purpose
The primary purpose is to provide automated batch processing of ipSAE calculations across multiple protein structure prediction runs. The script aggregates interface quality metrics from both AlphaFold3 and Boltz-2 prediction formats into a single summary CSV file.

### Key Innovations and Features

1. **Dual Source Support**: The script now handles two distinct protein structure prediction formats:
   - **AlphaFold3**: Processes `full_data_<i>.json` + `model_<i>.cif` file pairs in run subdirectories
   - **Boltz-2**: Navigates complex nested directory structures to find `pae_*.npz` + `*.cif` file pairs

2. **Batch Processing Pipeline**:
   - Discovers prediction runs in a root directory
   - Automatically runs `ipsae.py` for each model pair (with parallel execution)
   - Extracts binder→target ipSAE values from asymmetric interface rows
   - Aggregates statistics per binder (mean and standard deviation)

3. **Flexible Configuration**:
   - Configurable chain identifiers for binder and target chains
   - Adjustable PAE and distance cutoffs (with source-specific clamping)
   - Support for multiple chain-pair reduction strategies ("max" or "mean")
   - Optional filtering of Boltz-2 prediction types (target/self/antitarget)

4. **Performance Optimization**:
   - Parallel processing with configurable worker count
   - Smart caching - skips recomputation if output files exist (unless `--force` specified)
   - Deterministic ordering of model processing

### Architectural Changes
- Introduces a data class `ModelTask` to encapsulate processing parameters
- Modular design with separate discovery functions for each prediction source
- Clear separation between file discovery, ipSAE computation, and result aggregation
- Error handling with detailed logging for failed computations

### Notable Implementation Details
- The script handles the different file naming conventions between AF3 (`_full_data_*.json`) and Boltz-2 (`pae_*.npz`)
- For Boltz-2, it navigates through `outputs/boltz_results_*/predictions/*/` directory structures
- Output files are named with zero-padded cutoffs (e.g., `model_1_10_10.txt`)
- Statistical aggregation includes sample standard deviation for runs with ≥2 models

### Impact and Value
This script significantly improves workflow efficiency for researchers analyzing multiple protein-protein interaction predictions. By automating the batch processing of ipSAE calculations, it:
- Reduces manual effort in processing individual prediction runs
- Enables comparative analysis across different prediction methods (AF3 vs Boltz-2)
- Provides standardized statistical summaries for quality assessment
- Facilitates large-scale benchmarking of protein interface prediction accuracy

### Tags
- feature
- functionality
- improvement

**Commits:**

- [d02ea524](/commit/d02ea524a5487583a478d522bfae99c57850d0e0) - <span style="color:green">+540</span>/<span style="color:red">-0</span> (1 files): Add Boltz-2 support to summarize_ipsae.py [Aaron Ring <aaronring@gmail.com>]


---

### [AtharvaTilewale/IPSAE](https://github.com/AtharvaTilewale/IPSAE)

**Stats:**
- Commits ahead: 1
- Commits behind: 0
- Stars: 0

- Pull Requests:

  - [PR #1](https://github.com/DunbrackLab/IPSAE/pull/21)


- Last updated: 2025-11-19T18:31:03+00:00

**Summary of Changes:**
## Summary of Changes

The changes introduce significant improvements to the file format handling and robustness of the `ipsae.py` script, primarily focused on supporting both PDB and CIF file formats more consistently.

### Key Changes:

1. **Extended File Format Support**: Modified the file type detection logic to handle both `.pdb` and `.cif` files when paired with `.npz` PAE files. This allows the script to process structures in either format using the same code path.

2. **Enhanced CIF Parser**: Improved the CIF atom line parser to preferentially use `auth_asym_id` (author chain ID) over `label_asym_id` when available. This ensures better compatibility with different CIF file conventions.

3. **Robust pLDDT Handling**: Added intelligent scaling for pLDDT values by detecting whether they are normalized (≤1.0) or already in percentage scale (0-100). This prevents incorrect scaling when processing different pLDDT data formats.

4. **Error Handling Improvements**: Added fallback mechanisms for missing JSON keys (`pair_chains_iptm`) and better error messages, making the script more resilient to variations in input file formats.

### Technical Impact:
- **Backward Compatibility**: Maintains support for existing workflows while adding new capabilities
- **Format Flexibility**: Users can now use either PDB or CIF formats interchangeably with NPZ PAE files
- **Data Integrity**: Prevents incorrect pLDDT scaling and improves chain identification accuracy
- **Error Resilience**: Graceful handling of missing data keys prevents catastrophic failures

### Tags:
- functionality
- improvement
- bugfix

These changes significantly enhance the script's versatility and reliability when working with different structural biology file formats and data sources.

**Commits:**

- [efb00888](/commit/efb0088890082829561c33e61f84b84be6bc6f1c) - <span style="color:green">+25</span>/<span style="color:red">-9</span> (1 files): Update ipsae.py [Atharva Tilewale <tilewale.atharva@gmail.com>]


---



## Summary of Most Interesting Forks

After reviewing the forks, the most impactful contributions center on **packaging, performance, and cloud-scale execution**. The **y1zhou/IPSAE** fork stands out as the most comprehensive, transforming the monolithic script into a modular Python package with significant new functionality—most notably **user-defined chain group analysis** for flexible protein complex scoring, alongside robust input validation and vectorized calculations for speed. Similarly, **s-nitz/IPSAE** delivers a focused **performance boost through vectorization** and adds a solid testing suite, while **ullahsamee/IPSAE** provides a clean, pip-installable package with improved CLI and documentation, lowering the entry barrier.

For specialized use cases, **hemeai/IPSAE** introduces a **Modal Labs wrapper** for cloud-based batch processing, enabling scalable IPSAE runs on GPU infrastructure—valuable for large-scale structural bioinformatics. Meanwhile, **cytokineking/IPSAE** adds a **batch processing script** that automates analysis across AlphaFold3 and Boltz-2 predictions, streamlining workflows for researchers. Other forks offer useful incremental fixes, like **QVQuality/IPSAE**'s custom output directory and edge-case bug fix, and **AtharvaTilewale/IPSAE**'s improved file format handling. Overall, the most notable forks enhance the tool's core architecture, performance, and scalability, making it more robust and adaptable for modern computational biology pipelines.
 