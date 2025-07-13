# CUL

## Table of Contents
⁃ [What is CUL?](#what-is-cul)<br>
⁃ [Why Choose CUL Over Other Package Managers?](#why-choose-cul-over-other-package-managers)<br>
⁃ [Features](#features)<br>
⁃ [How to Install?](#how-to-install)<br>
⁃ [How to Use?](#how-to-use)<br>
⁃ [How to Contribute?](#how-to-contribute)<br>
⁃ [A Little Backstory](#a-little-backstory)<br>

---

## What is CUL?

CUL is a command-line utility for the C/C++ programming language that simplifies the downloading and management of external modules (header files).  

Inspired by Python's pip and NodeJS's npm, the goal of CUL is to provide an efficient and user-friendly way to manage project-specific header files, making them easier to download, update, and organize.

CUL is not just a **standalone project**—it is **a part of a larger vision** to create a **complete ecosystem** for **C/C++ development.** Once CUL reaches a stable state with all planned features, the next phase will begin: building a modular ecosystem that enhances the way developers manage dependencies, build projects, and streamline development in C/C++.

The modules are stored in a separate repository along with the code of the backend file server, which can be accessed here: [CUL Backend](https://github.com/atrithakar/cul_backend_fastapi_mongodb).

## Why Choose CUL Over Other Package Managers?
Most C/C++ package managers are **either too complex or too limited**. **CUL is here to change that!**  
CUL is **built for developers, by a developer** to make C/C++ package management as **easy as Python’s pip or JavaScript’s npm!** 🚀
<br>Here's how CUL compares to other well-known C/C++ package managers. This comparison reflects CUL's current capabilities, not future planned features.

| **Feature**                    | **CUL 🚀** | **Conan 🏗️** | **vcpkg 🏢** | **Hunter 🏹** | **Spack 🔬** |
|---------------------------------|------------|--------------|--------------|--------------|--------------|
| **Ease of Use 🏆**              | ✅ Intuitive CLI (pip/npm-like) | 🟡 Moderate learning curve | ✅ Easy, Visual Studio-friendly | 🟡 Moderate, CMake-centric | ❌ Complex, HPC-focused |
| **Platform Support 💻**         | ✅ Cross-platform | ✅ Cross-platform | ✅ Cross-platform | ✅ Cross-platform | ✅ Cross-platform |
| **Repository Size 📚**          | 🆕 Growing | 📦 Large | 📦 Large (Microsoft) | 📦 Moderate | 🏢 Extensive (scientific) |
| **Build System Independence 🏗️❌** | ✅ Works standalone | ❌ Requires CMake | ❌ Requires MSBuild/CMake | ❌ CMake-focused | ❌ Complex build scripts |
| **Versioning Support 🔢**       | ✅ Available | ✅ Yes | ⚠️ Limited | ✅ Yes | ✅ Yes |
| **Dependency Resolution 🔄**    | ✅ Automatic | 🔥 Advanced | ⚠️ Basic | ⚠️ Manual setup | 🔥 Advanced |
| **Caching Mechanism 📀**        | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Custom Repositories 🌍**      | ✅ Multi-registry | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Fuzzy Search 🔍**             | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Community Support 🤝**        | 🚀 Emerging | 💬 Active | 🏢 Microsoft-backed | 💬 Small but active | 🔬 Research-focused |
| **Documentation 📖**            | ✍️ Comprehensive, evolving | 📜 Extensive | 📜 Detailed | 📜 Moderate | 📜 Extensive |
| **Binary Packages 📦**          | ⏳ Planned | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Security 🔒**                 | ⏳ Planned | ✅ Yes | ⚠️ Basic | ⚠️ Basic | 🔥 Advanced |
| **Offline Installation ✈️**     | ✅ Supported via caching | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Lightweight ⚡**               | ✅ Yes | ❌ Heavy | ❌ Bloated | ✅ Yes | ❌ Complex setup |
| **Error Logging 📜** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Learning Curve 📈**           | ⭐ Gentle, beginner-friendly | 📉 Moderate | ⭐ Easy | 📉 Moderate | 📉 Steep |

---
## Features:
- Provides minimalistic UI.
- Installs modules directly into project directory.
- Allows searching for the versions availabe, if any, before installing the module.
- Uses caching technique to install the module again in less amount of time without using the internet.
- Provides a way to list all the modules installed, both in human readable way and machine readable way, and store them into a .txt file.
- Allows downloading different versions of modules.
- Provides the way to initialize a project and maintain dependencies/requirements easily.
- Installs all the required modules by the current installing module automatically.
- Users can search for a module even if they know only a part of its name.
- Automatically logs warnings and errors in a .cul folder inside the project folder for ease of access.
- Modules can be downloaded from various registries hosted and maintained by independent individuals or organizations.

---

## How to Install?

Installation Guide: [Click Here](https://github.com/atrithakar/project_cul/blob/main/MDs/installation_guide.md)

---

## How to Use?

User Manual: [Click Here](https://github.com/atrithakar/project_cul/blob/main/MDs/user_manual.md)

---

## How to Contribute?

CUL is an open-source project, and contributions from the community are highly welcome!  

If you have the skills and passion to improve this tool, feel free to contribute. All contributions will go through a thorough code review process before being approved.

### Steps to Contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes and create a pull request.
4. Wait for the code review and approval.

---

Thank you for contributing to CUL and making it better!

Feel free to share feedback or report issues in the [GitHub Issues](https://github.com/atrithakar/project_cul/issues) section. Let's make C/C++ module management hassle-free together!

---
## A little backstory:
During my early college days, I began learning Python after gaining experience with the C language. I often wondered why C didn't have a package management tool like Python's pip, which sparked an idea in me to create one. This project became my dream, motivated by my love for programming rather than the pursuit of fame or financial success.  

At that time, I was unaware of existing tools like vcpkg and Conan that provide package management for C/C++. Instead of feeling discouraged by their existence, I found inspiration in them to improve my own tool, CUL. Initially, my plan was to implement basic functionalities such as installing, uninstalling, updating, and providing help. However, as I worked on the project, my desire to enhance its capabilities grew.  

One particular incident during college strengthened my resolution to build CUL. A faculty member once gave our class a fun little activity and hinted that we could use `graphics.h` to complete it. Excited to experiment, I jumped in, only to find myself stuck battling linker errors for hours. The process of manually setting up external dependencies in C felt unnecessarily tedious compared to Python or other modern languages. That frustration stuck with me, and I knew there had to be a better way.  

That experience, along with countless other struggles of dealing with dependencies in C/C++, reinforced my belief that a package management tool for C/C++ should exist. I continue to develop CUL with the hope of making it a valuable resource for others in the C/C++ community. I recognize the many excellent tools available and aim to learn from them while striving to contribute positively to the ecosystem. This journey is about growth, learning, and sharing knowledge within the programming community—turning past frustrations into a solution that benefits others.