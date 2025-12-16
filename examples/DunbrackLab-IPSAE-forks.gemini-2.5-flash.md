# Fork Analysis Report for DunbrackLab/IPSAE

Repository: [DunbrackLab/IPSAE](https://github.com/DunbrackLab/IPSAE)

Description: Scoring function for interprotein interactions in AlphaFold2 and AlphaFold3

Stars: 171
Generated: 2025-12-16 10:51:29 UTC

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
This fork introduces a significant overhaul and enhancement of the `ipsae` script, transforming it from a standalone utility into a more robust, maintainable, and feature-rich application. The core purpose

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
This fork introduces substantial changes primarily focused on transforming the original `ipsae.py` script into a well-structured, pip-installable Python package.

### Summary of Changes and Innovations

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
This fork introduces significant architectural changes and performance improvements to the `ipsae` calculation logic, along with enhanced testing and input handling.

### Summary of Changes and Innovations:

1.  **

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
This fork introduces foundational changes aimed at improving the project's **deployability, reproducibility, and automated release management** through containerization and CI/CD.

**Summary of Changes and Innovations:**



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
This fork introduces a significant innovation by integrating the DunbrackLab IPSAE (Inter-Protein Spatial-Atomic Environment) calculation tool with Modal Labs for cloud-based, scalable execution. The core change is

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
This fork introduces a focused set of changes aimed at enhancing the usability, robustness, and code quality of the application, particularly around the `ipsae.py` script.

### Summary

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
This fork introduces significant enhancements to the `ipsae.py` script, primarily focusing on its capability to process protein-ligand complexes. The changes include adding support for handling ligands alongside proteins

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
This fork introduces a significant architectural overhaul, transforming a monolithic `ipsae.py` script into a structured, modular Python library. The project appears to be focused on the analysis and visualization of protein

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
This commit introduces a new Python script, `summarize_ipsae.py`, designed for batch processing and summarizing ipSAE (interface predicted aligned error) values from structural prediction runs.

### Summary of Changes and Innovations:

1.  **Main Themes and Purpose:**
    *   **Automated ipSAE Summarization:** The primary goal is to automate the extraction, calculation, and summarization of ipSAE across numerous AlphaFold 3 (AF3) or Bol

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
This commit introduces several improvements to the `ipsae.py` script, primarily focused on enhancing its compatibility with various input file formats and improving the robustness of data parsing and handling, especially for models generated by AlphaFold-

**Commits:**

- [efb00888](/commit/efb0088890082829561c33e61f84b84be6bc6f1c) - <span style="color:green">+25</span>/<span style="color:red">-9</span> (1 files): Update ipsae.py [Atharva Tilewale <tilewale.atharva@gmail.com>]


---



## Summary of Most Interesting Forks

Several forks introduce significant enhancements that could greatly benefit the main repository, ranging from architectural overhauls to new capabilities and improved deployability.

The most impactful forks include:

*   
 