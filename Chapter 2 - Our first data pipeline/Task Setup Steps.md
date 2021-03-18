# Useful steps to create a specific task.

1). Write the python code.

It is important to remember a few important things:
* Make sure the correct operator or provider packages are installed, using ```pip install <operator_string>```
* Make sure you remember to import the operators using ```import```.
* Make sure you're aware of the basic default arguments and they're all parameterised.
* Check code for mistakes.

2). Open up the UI & Scheduler from the python env (with the following commands):

```airflow webserver```\
```airflow scheduler```

And check whether the DAG has been imported properly, there will be a warning if not. You should be able to click on your DAG & see whether the task is present.

3). Configure the new connection for the task.

Go to:

Admin -----> Connections -----> New

A few things to double check:

* Ensure the connection name matches the conn_id you specify in the python code.
* Ensure you have the correct type of connection, i.e. a HTTP or SQLite.

4). Test the new task from the Airflow CLI using:

```airflow tasks test <dag_id> <task_id> <execution_date>```

You should get a SUCCESS if configured correctly.

5). Validate the test if possible.