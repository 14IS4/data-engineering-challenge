## Data Engineering Challenge

Thank you for taking the time to complete this assignment. We believe this to be an effective way to showcase your skills, on your own time, without the pressure of someone looking over your shoulder. Your code will help us decide if we'd like to proceed with the interview process. Please understand that follow up interviews are not guaranteed upon completing this assignment. However, we will keep you posted either way.


_Even though there is no strict time limit, it should take you ~4 hours to complete the assignment. Have fun!_

## Objective

**Write a python script that ingests data from one of the external vendor's data sources and combine that data with our internal data set.** This combined data set should allow data team members to compare the active users of the different platforms.

## Requirements


1. The script can run in an environment with limited amounts of memory. The final solution should avoid reading all the rows from either source at one time. For example, reading in 10% of database rows and 10% of API rows and then do the matching would be acceptable. Reading in 100% of either source prior to matching would not be acceptable.
2. Pretend that the current date is 2017-02-02. There are references in the assignment that will confirm that as the "current" date.
3. The script should finish in under **15** minutes. If the script takes longer, please explain any challenges and complexities in meeting this requirement in the feedback.txt.
4. Make sure submission contains all the items outlined in [What to Submit](#what-to-submit)

## Details from Product Manager

Hey DE,

A vendor (Friendly Vendor) recently agreed to make their data available for us to use. Their dataset includes their users and information about whether or not the user is currently active (active within the last 30 days) on their platform. We plan on using their user data combined with our user data to measure the health of the two business. This will potentially let us predict churn on our platform based on the user's activity on Friendly Vendor's platform (if there is a correlation).

Our immediate use case requires having both sets of users and their active status from the two platforms matched up and available in our warehouse. If we establish a correlation between the two platforms then I'm confident we will want to start gathering more data.

As you build out your pipeline please keep in mind that both platforms expect their user bases to expand significantly over the upcoming year.

Below is the email I received from Friendly Vendor about the different ways of retrieving the data:

## Email from Friendly Vendor

Hey --------,

We have arranged for you to have access to our data! We don’t have any authentication requirements to access the data so you can directly access the following API publicly.

[User Activity API](http://de-tech-challenge-api.herokuapp.com/api/v1/users)

This REST API endpoint contains our users and their activity status. Add `?page=X` at the end of the URL to page through the users. For example `http://de-tech-challenge-api.herokuapp.com/api/v1/users?page=3` to view the third page. This directly accesses our database and we plan on creating new endpoints (such as v2, v3, etc.) if we want to make any breaking changes in the future.

Thanks,

Friendly Vendor

## Connection Information for MySQL instance:

**Host:** --------

**Username:** `de_candidate`

**Password:** --------

**Port:** `3316`

**Schema:** `data_engineer`

**Tables:** `user`, `user_practice`

## Expected Output from Python Script:

**Elapsed Time:** `X minutes, X seconds` *<- Time it took to run the entire script*

**Total Matches:** `X` *<- Total number of rows matched between the -------- dataset and the vendor dataset*

**Sample Output:** `<10 JSON formatted rows>` *<- Example of the rows that would be loaded to the warehouse*

**SQL DDL:** `CREATE TABLE…` *<- The DDL that would have been used to create the warehouse table. The overall table structure is what we will look at, this doesn't actually have to run.*

## What to Submit

1. The Python script(s) you wrote to solve this problem.
2. A `requirements.txt` file containing a list of packages required to run your script.
3. An `output.txt` file containing the output from your script that matches the expected output above.
4. An `instructions.txt` file containing instructions on how to run your submission.
5. A `feedback.txt` file describing how you would productionize this code. You may include a section containing any thoughts or feedback from the assignment or anything you would like the reviewers to consider when reviewing. (Optional) If you are making any assumptions please include them here.


## Starting your assignment
Our assignments are published on gitlab and our reviews are done by viewing submissions in gitlab. You can brush up on git and gitlab [here](https://docs.gitlab.com/ee/gitlab-basics/).

1. Fork the data-engineering repository by visiting [this page](https://gitlab.com/interview-assignments/data-engineering/-/forks/new) and selecting your namespace.
 * If you experience access errors after logging in, please reach out to your recruiter contact for help.
2. Create a development branch and download the forked repo in order to begin development.
	- Visit `https://gitlab.com/<YOUR_USERNAME>/data-engineering/branches` (replace YOUR_USERNAME with your gitlab username)
	- click `New Branch` and name your branch <firstname>-<lastname>.
3. Clone your forked repo locally to begin development.
	- In your new branch, click the blue `Clone` button.
	- Copy to clipboard the contents of `Clone with HTTPS` box.
	- Open a terminal window and clone the repo using git. `git clone https://gitlab.com/<YOUR_USERNAME>/data-engineering.git`
	  - authenticate using your gitlab credentials.

## Submitting your assignment

1. Add -------- as a member to your assignment.
	- Visit `https://gitlab.com/<YOUR_USERNAME>/data-engineering/-/project_members`
	- Enter --------- for Gitlab member box.
	- Select Reporter as the role.
	- Click Invite.
2. Create a merge request from your development branch. NOTE: we only need a merge request created and not an actual merge performed.
	- Visit` https://gitlab.com/<YOUR_USERNAME>/data-engineering/edit` 
	- Under Visibility, project features, permissions enable `Merge Requests` and hit Save.
	- Visit `https://gitlab.com/<YOUR_USERNAME>/data-engineering/-/tree/<YOUR_BRANCH_NAME>`
	- Click the blue `Create merge request` button.
	- Enter Title and Description, then select -------- from the `Assignee` dropdown box.
	- Click `Submit merge request`.
	- Notify your recruiter contact that your submission has been submitted and is ready for review.
* If you experience issues at this stage, please reach out to your recruiter contact for help.


**If any questions come up, please send an email to your -------- point of contact.**

## What to Expect After You Submit
Our reviewers team will be notified and review your submission within 3 days. We will check that your submission installs and runs as guided by the instructions.txt. We will evaluate the submission based on
- Ability to follow directions, both on accomplishing the functionality as well as the logistics around assignment submission.
- Code quality, style, standards, simplicity, and consistency as well as ease of maintenance.
- Performance and scaling considerations.
- Output based on the matching solution used. The matching requirements are open ended on purpose - we will evaluate results based on the matching solution employed.

We know your time is valuable and appreciate you taking the time to complete this assignment.
