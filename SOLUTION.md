# DE Challengue Solution

---


## Requirements Resume

* The programming language must be Java, Scala or Python.
* A consumption data model must be created, expected in 3NF.
* Generate the data model, and save it with a specific format and as image.
* Generate some reports like:
  * The top 10 best games for each console/company.
  * The worst 10 games for each console/company.
  * The top 10 best games for all consoles.
  * The worst 10 games for all consoles. The data is in the folder data/ in the root. 
  The report can be exposed in any way you want, but remember this is an ETL Job.
* The deployment must work on any environment

## Restrictions and BU Rules

* GCP can be used
* ELT Approach can be used

---

## Data architecture diagram

Based on the previous requirements, I designed three types of architectures 
with a resume of the problems and why would I choose it.

The following was the chosen one:

![alt text](img/architecture.png)

This architecture works as event driven, the ETL Job is executed in the exact moment that a file arrives
into the system, but it has some problems like:

* Reports complexity construction
* Multi dependency files to build a report
* Only append - no dedup strategy

But it has some good things like:

* Reports executed in the moment of the arrival of the file.
* Reports already processed saved as files and tables.

*About the other diagrams*:

https://lucid.app/lucidchart/3bdfd770-c1cc-4921-8986-bd8602bc7404/edit?invitationId=inv_e7c9d347-d92b-4c51-ac93-e8b5307dec7e

## Resume & Workflow


## Steps to reproduce
