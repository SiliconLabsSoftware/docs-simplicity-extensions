# External Repositories

Simplicity Studio provides functionality to work with external repositories, which can be useful for accessing example projects and collaborating with teams.

## Creating a Simplicity Studio compatible external repository

Simplicity Studio provides funtionality to work with external Git repositories and load, and show example applications in the Launcher view like any other example applications provided by the Silicon Labs SDKs and SDK extensions.
The external repository should contain the example applications, and a templates.xml file which lists all of the provided applications.

The source files for this external repo created in this tutorial is available on GitHub [here](https://github.com/SiliconLabsSoftware/docs-simplicity-extensions).

### Recommended folder structure
- **your_git_repository**
  - example_a
    - inc
    - src
    - config
    - example_a.slcp
    - README.md
  - example_b
    - inc
    - src
    - config
    - example_b.slcp
    - README.md
  - templates.xml

## Create a new Git repository (locally)

- [Getting a Git Repository](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)

## Project file (\*.slcp) creation

In this tutorial we are creating a simple external repository with an example application and a templates.xml file. 

Create the following folder structure:

-**your_git_repository**
  - external_repo_example_soc_app
    - inc
    - src
    external_repo_example_soc_app.slcp

Follow the guide below to create and validate an .slcp project files.
 - [Create and validate .slcp project files](./EXTENSION.md#create-example-project)

The sample external_repo_example_soc_app.slcp file:

```yaml
project_name: external_repo_example_soc_app
quality: production
label: My Extension - SoC Example App (External Repo)
description: "This example project shows how to blink an LED in a bare-metal configuration. Or with a CLI command"
category: Example|My Extension

source:
  - path: src/app.c
  - path: src/main.c
  - path: src/blink.c
include:
  - path: inc
    file_list:
    - path: app.h
    - path: blink.h

sdk_extension:
  - id: my_extension
    version: 1.0.0

component:
  - id: sl_system
  - id: device_init
  - id: sleeptimer
  - id: simple_led
    instance: [led0, led1]
  - id: cli
    instance: [example]
  - id: printf
  - id: iostream_recommended_stream
  - id: sample_component_info
    from: my_extension

requires:
  - name: iostream_retarget_stdio

define:
  - name: DEBUG_EFM
readme:
  - path: doc/readme.md
ui_hints:
  highlight: readme.md

configuration:
  - name: SL_BOARD_ENABLE_VCOM
    value: "1"
  - name: SL_CLI_LOCAL_ECHO
    value: "(1)"
  - name: SL_IOSTREAM_USART_VCOM_CONVERT_BY_DEFAULT_LF_TO_CRLF
    value: "(1)"
  - name: SL_IOSTREAM_USART_VCOM_FLOW_CONTROL_TYPE
    value: "usartHwFlowControlNone"
  - name: SL_IOSTREAM_EUSART_VCOM_CONVERT_BY_DEFAULT_LF_TO_CRLF
    value: "(1)"
  - name: SL_IOSTREAM_EUSART_VCOM_FLOW_CONTROL_TYPE
    value: "eusartHwFlowControlNone"
  - name: SAMPLE_APP_NAME
    value: "Example Sample application"

template_contribution:
#------------------ CLI commands ---------------------
  - name: cli_command
    value:
      name: toggle
      handler: toggle_led
      help: Toggle the LED1

tag:
  - hardware:component:led:2+
  - hardware:component:vcom

filter:
  - name: "Device Type"
    value: ["SoC"]
  - name: "MCU"
    value: ["32-bit MCU"]
  - name: "Project Difficulty"
    value: ["Beginner"]
```

Copy the given source, header and readme files from the [repository](https://github.com/SiliconLabsSoftware/docs-simplicity-extensions) to the their defined folders in the sample application root folder.

### Generate templates.xml

In the [example repository](https://github.com/SiliconLabsSoftware/docs-simplicity-extensions) you will find a python script which will generates this xml file, under *tools/template_xml_generator.*

First step install the ```requirements.txt``` file for Python. 

**Install requirements**

```shell
python3 -m pip install -r requirements.txt
```

Generation CLI command, where ```\--extension-root``` is the path of your extension and ```\--output-directory``` is the path where the xml will be generated.

**Example generator call**

```shell
python3 main.py --extension-root external_repo_root_folder --output-directory my_output
```

The script will look for all the ```\*.slcp``` files in your extension folder and create a template xml. You have to manually update two fields: ```boardCompatibility``` and ```partCompatibility```. These fields are regex values, by default all boards and parts are enabled. Which means Simplicity Studio will show the application for all targets. 

The sample templates.xml file:

```XML
<?xml version='1.0' encoding='ASCII'?>
<model:MDescriptors xmlns:model="http://www.silabs.com/ss/Studio.ecore">

  <descriptors name="example_app" label="My Extension - SoC Example App (External Repo)" description="This example project shows how to blink an LED in a bare-metal configuration. Or with a CLI command">
    <properties key="namespace" value="template.uc"/>
    <properties key="keywords" value="universal\ configurator"/>
    <properties key="solutionReferenceId" value="external_repo_example_soc_app.external_repo_example_soc_app.slcp"/>
    <properties key="projectFilePaths" value="external_repo_example_soc_app\external_repo_example_soc_app.slcp"/>
    <properties key="readmeFiles" value="doc/readme.md"/>
    <properties key="boardCompatibility" value=".* com.silabs.board.none"/>
    <properties key="partCompatibility" value=".*"/>
    <properties key="ideCompatibility" value="iar-embedded-workbench makefile-ide simplicity-ide visual-studio-code"/>
    <properties key="toolchainCompatibility" value="gcc iar segger"/>
    <properties key="category" value="Example|My Extension"/>
    <properties key="quality" value="PRODUCTION"/>
    <properties key="stockConfigCompatibility" value="com.silabs.ss.framework.project.toolchain.core.default"/>
    <properties key="filters" value="Device\ Type|SoC MCU|32-bit\ MCU Project\ Difficulty|Beginner"/>
  </descriptors>

</model:MDescriptors>
```

Add and commit your changes to your git repository:

```shell
git add *
git commit -m "First example application"
```

Now you have a Git repository which contains an example application. This repository is ready to use as an external repo in Simplicity Studio. 

## Adding external repositories in Simplicity Studio

- Go to Preferences > Simplicity Studio > External Repos
- Here you can add, edit, and delete repos
- To add a repo, you first clone it and then select the branch, tag, or commit to add
- The default branch is usually "master" or "main"


## Using external repositories

- Once added, these repos will appear under the "EXAMPLE PROJECTS & DEMOS" tab in the Launcher
- You can filter by the repo name (e.g., "bluetooth_applications" or "platform_applications") to see relevant examples
- Click CREATE on a project to generate a new application from the selected template


## Documentation
- [Simplicity Studio 5 Users Guide](https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-about-the-launcher/welcome-and-device-tabs#example-projects-demos-tab)

## Silicon Labs External Repositores

- [Bluetooth Applications](https://github.com/SiliconLabs/bluetooth_applications.git)
- [Peripheral Examples](https://github.com/SiliconLabs/peripheral_examples)
- [Platform Applications](https://github.com/SiliconLabs/platform_applications.git)
- [Zigbee Applications](https://github.com/SiliconLabs/zigbee_applications)
- [Wi-Fi Applications](https://github.com/SiliconLabs/wifi_applications)