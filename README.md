# quiz_generator
A tool that uses a LLM to generate questions for an exam, based on a set of documents.
<br>
Targeted to the Italian language.  UI messages and prompts to the LLM are written in Italian.<br>

## Installation of the required packages

The requirement.txt for a given project is either in the root directory of the repository.<br>
The environment is, for example, in a directory called <code>env</code>. To create it:<br>

<code>
<pre>
    python3 -m venv ./venv

    source venv/bin/activate  # Activate the environment

    sudo apt-get install pipx         # Needed by poetry
    pipx install poetry               # Poetry
    pip  install -r requirements.txt  # Installs the packages listed in requirements.txt
</pre>
</code>


### Environment activation
Activate the environment with the command:

<code>
<pre>
  # cd to the root directory of the towards_ai_course repo
  export REPO_ROOT=$(pwd)
  export DATASET_ROOT=${REPO_ROOT}/dataset
  export STORAGE_ROOT=${REPO_ROOT}/storage

  source venv/bin/activate

  source ${REPO_ROOT}/api_keys/api_keys.sh

  export PYTHONPATH=${PYTHONPATH}:${REPO_ROOT}/src_py/lib
</pre>
</code>

Run using the command:
<code>
<pre>
  python3 ${REPO_ROOT}/src_py/main_tk_ui.py
</pre>
</code>

Execution example:
<img src="images/screen_shot.jpg" alt="UI image"/>

