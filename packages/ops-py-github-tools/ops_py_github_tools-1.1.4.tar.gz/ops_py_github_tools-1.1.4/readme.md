# ops-py-github-tools

## Description 
A collection of various GitHub Tools:    
  - Create or get GitHub Repo Milestones
  - Get GitHub repo Pull Requests info    
  - Create GitHub repo issue templates      
  - Perform requests to GitHub

    
## Installation `pip install ops-py-github-tools`      

## Usage    
  Please refer to [github_tools_examples.py](src%2Fgithub_tools%2Fgithub_tools_examples.py)


### Create desired template based on the title of the GitHub Issue

**Example:**   
```
python3 -m github_tools.github_issue_templates --title "📇 mc-isb: Monitoring documentation" --templates_dir .github/ISSUE_TEMPLATE \
     --template_filenames c_epic.md c_epic_maintenance.md d_collection.md d_collection_maintenance.md e_task.md --team_alias myt --team_name "My Team" \
     --team_alias_placeholder "<team_alias>" --team_name_placeholder "<team_name>" \
     --write_templates "" --templates_version v2.0.1 > template.md
```

**Example output:**     
``` 
cat template.md 
---
name: "\U0001f4c7 Collection"
about: "Group(s) of tasks"
title: "\U0001f4c7 c-myt:"
version: "v2.0.1"
---

## Purpose

> Remember the goal type of your tasks here. If any existing tasks are related to another :trophy: Goal type, they should be moved to respective :crown: Epic ->  inside that specific :card_index: collection.

### Summary

DevOps link: `none` / AB#ticketNumber

This collection includes tasks related to..... <!-- Summarise overall reason for tasks in this collection -->

#### Acceptance Criteria

- None

#### Task(s)

- [ ] None

#### Pull Requests

- [ ] None


```