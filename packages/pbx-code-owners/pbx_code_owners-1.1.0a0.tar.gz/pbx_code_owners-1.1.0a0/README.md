# PBX Code Owners

Simple implementation of Code Owners feature available only in Gitlab Premium and Ultimate plans.


Sample configuration file (place it in main repo folder with name `codeowners.yml`):
```
sections:
  - name: "Your section name"
    paths:
      - "."
    owners:
      - '@have'
      - '@a_nice'
      - '@day'
  - name: "tests"
    paths:
      - "tests/"
    owners:
      - '@ninja_qa'
```



### Usage example:

Download package with pip, and execute script with command `pbx-code-owners`. 

Make sure you have all necessary environmental variables in scope:
* CI_SERVER_URL (eg. https://yourcompany.gitlab.com)
* CI_PROJECT_ID (can be found in project settings)
* CI_MERGE_REQUEST_IID (merge request ID)
* CODE_OWNERS_GITLAB_TOKEN (access token necessary for creating threads)
