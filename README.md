![goodfaith](img/goodfaith.png)

# goodfaith

### Hack within program scope

## Why goodfaith?
Recon automation continues to increase in popularity. Automation frameworks range anywhere from a complex, scalable cloud environment to a one-liner bash script. Both approaches are powerful, yet the techniques result in massive amounts of output.

What is the next step? What happens with this output?

At this point, the recon automation may have a combination of recursive sources, archived paths, and URLs pointing to third-party destinations. The next step is to begin fuzzing headers, verbs, paths, and parameters.
How do we move to fuzzing without manual review? This was a discovered gap proving to be a barrier when moving between recon and discovery to enumeration.

There will likely remain a manual intervention point although our goal is to push this further right and reduce the steps causing pipeline delays.

There are several public bounty program lists available although not all of them include out-of-scope items. Generating traffic against explicitly out-of-scope targets may result in damage to the company through availability impacts or outages, it could result in researcher program/platform bans, lost bounties, or worst case - legal consequences. To reduce the likelihood of testing against out-of-scope targets, a security researcher can now demonstrate proactive intent to hack with goodfaith.

This tool solves these major barriers towards scalable automation.
1) goodfaith can be imported into an existing project or utilized as a standalone bash script.
2) goodfaith can be proactively inserted into bug bounty one-liner chains to maintain scope throughout a workflow.
3) goodfaith handles explicitly out-of-scope targets.

## Installation
`goodfaith` can be installed using Python Pip with the following command:
```
pip3 install goodfaith
```
## Usage

