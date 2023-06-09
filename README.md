# Integration of face tracking and human-machine interaction with the ChatGPT API on the head of the INMOOV robot

![img](/images/inmoov.png)

**_This is my 4th year project in the service robotics major at CPE Lyon_**

![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![OpenAI](https://img.shields.io/badge/OpenAI-FF5A00?style=for-the-badge&logo=openai&logoColor=white)

## Authors

- **_Perrichet Theotime_**

## Abstract

This project aims to develop a solution for using the INMOOV robot head to perform face tracking and establish human-machine interaction using the ChatGPT API. The aim is to enable the robot to detect and track human faces and then interact with users using an advanced language model based on the ChatGPT API. This project combines the robot's visual recognition capabilities with natural language processing techniques to create a natural interaction between man and machine.

## Table of contents

- [Integration of face tracking and human-machine interaction with the ChatGPT API on the head of the INMOOV robot](#integration-of-face-tracking-and-human-machine-interaction-with-the-chatgpt-api-on-the-head-of-the-inmoov-robot)
  - [Authors](#authors)
  - [Abstract](#abstract)
  - [Table of contents](#table-of-contents)
  - [Youtube links](#youtube-links)
  - [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Services used](#services-used)
  - [Features](#features)
  - [Use](#use)
    - [1. create an OPENAI token](#1-create-an-openai-token)
    - [2. Create 2 text files](#2-create-2-text-files)
    - [3. Arduino codes](#3-arduino-codes)
    - [4. Run the program](#4-run-the-program)
  - [Diagram](#diagram)
  - [Todo List](#todo-list)
  - [References](#references)

## Youtube links

the [youtube](https://www.youtube.com/playlist?list=PLxonWIbIdwC61nbJOSWWsmZ7bKpfgkA30) link to the Pitch and Tutorial of the project

## Installation

**Creating a virtual environment:**

```bash
python3 -m venv env_inmoov
source env_inmoov/bin/activate
```

**Installation of Python libraries:**

```bash
pip install -r requirements.txt
```

## Prerequisites

- INMOOV robot (head)
- A camera
- a microphone
- 2 Arduino
- OpenAI account

## Services used

- [ChatGPT](https://openai.com/chatgpt)
- [Whisper](https://openai.com/research/whisper)
- Google Translate's text-to-speech API

## Features

- [x] Followed by face :
  - [x] Face detection
  - [x] Face tracking

- [x] Human-machine interaction with the ChatGPT API
  - [x] Speech To Text
  - [x] Text to Speech
  - [x] ChatGPT

- [x] Mouth movement as a function of audio

- [x] Using 2 Arduino :
  - [x] Arduino 1: Head movement management
  - [x] Arduino 2: Mouth movement management

## Use

### 1. create an OPENAI token

See this [link](https://platform.openai.com/docs/api-reference/authentication)

### 2. Create 2 text files

- an mpd.txt file: contains the OpenAI token
- an organisation.txt file: contains the organisation of the OpenAI account

Place them in the API folder

### 3. Arduino codes

- Upload the ***inmoov_jaw.ino*** code to the arduino controlling the mouth
- Upload the ***face_detector.ino*** code to the arduino controlling the robot head

### 4. Run the program

```bash
python3 conversation.py #starts conversation with chatGPT
```

```bash
python3 face_detector.py #starts face detection
```

## Diagram

![Diagram](/images/diagram.png)

## Todo List

- [x] Create a virtual environment
- [x] Making **STT**(Speech To Text) and **TTS**(Text To Speech) in the cloud
- [ ] Running Text to Speech locally
- [x] Make a code to carry out a conversation with ChatGPT
- [x] Produce a program combining the various functions of the robot using multiprocessing.
- [x] Make the robot's mouth move according to the amplitude of the audio.
- [ ] Ensure that audio and mouth movement are coordinated
- [ ] Using a single Arduino

## References

- <https://inmoov.fr/head-3/>
- <https://github.com/The-Assembly/Build-A-Face-Tracking-Camera-With-Computer-Vision>
- <https://platform.openai.com/docs/api-reference/chat/create>
- <https://pypi.org/project/playsound/1.2.2/>
