# CSCI5801 SE I - Phase 4 Scrum

## Project Overview
This repository contains our Phase 4 project for bug verification, unit testing, and Scrum process documentation for the LISCO chess system.

The main goal of this phase is to test the provided chess implementation, identify defects based on the given specification, and maintain clear records of project progress throughout the sprint.

## Team:

Group 7

## Team Members
- Benat Froemming-Aldanondo
- Blein Bekele
- Jyothsna Mysore Santhosh Kumar
- Reshma Rao Chandukudlu Hosamane

## Backlogs

The Product Backlog and Sprint Backlog are maintained in a shared Google Sheet.

- [View Product and Sprint Backlog status](https://docs.google.com/spreadsheets/d/1sV1Uap7xQDlHYhp4MC6lu6gxwZQAZ8Uj2NT8FR2hmAg/edit?usp=sharing)

## Repository Structure

```text
├── README.md
├── Chess Logic Files/
│   ├── spell_logic.py
│   ├── test_spell_logic.py   #Contains the test functions
│   ├── SPELL_CHESS_RULES.md
├── meetings/
|   ├── Sprint Planning Meeting.md
|   ├── Scrum Meeting 1.md
|   ├── Scrum Meeting 2.md
|   ├── Scrum Meeting 3.md
|   ├── Sprint Review Meeting.md
|   ├── Sprint Retrospective Meeting.md
├── reports/
|   ├──test_execution_report.txt

```
# Instructions to Build and Run the Program

## System Requirements

- Python 3.10 or higher

## Installation

Install the required dependencies:

```bash
pip install pytest chess
```
## Running all the tests:

```bash
cd "Chess Logic Files"

python -m pytest test_spell_logic.py -v
```
## Save Test Execution Report

To save the test results to a file, run:

```bash
python -m pytest test_spell_logic.py -v > ../reports/test_execution_report.txt
```
## Expected Behavior

- All test cases will execute successfully.
- Some test cases are expected to **fail**.
- Failed tests indicate **defects in the provided implementation**.

## Test Coverage

The test suite covers:

- Standard chess rules (movement, captures, special moves)
- Freeze spell (charges, cooldown, duration, movement restriction)
- Jump spell (movement rules, restrictions, cooldown)
- Game state display (turn indication, check detection, spell info)

These tests are derived directly from the specification (`SPELL_CHESS_RULES.md`).
