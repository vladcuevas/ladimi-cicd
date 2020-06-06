# ladimi-aws

CI/CD Django project to work with Elastic BeanStalk (eb) and AWS CodePipeline.

## Requirements

1. Configure [AWS account](https://aws.amazon.com/)
2. [AWS CLI version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
3. AWS Elastic Beanstalk Command Line Interface ([EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html))
4. Python [3.7.7](https://www.python.org/downloads/release/python-377/)

## Configuration

1. From a terminal, install [pipenv](https://github.com/pypa/pipenv)

    ```powershell
    pip install pipenv
    ```

2. Execute the below commands:

    ```powershell
    pipenv shell
    pipenv update
    ```

    _Command pipenv shell will create virtual environment if it is not created. Command pienv update will install the packages contained in file [Pipfile](Pipfile)_

3. [optional] If new packages are added, execute the below command from the Django project folder (i.e ladimi), instead of the root folder of the [Git](https://git-scm.com/) repository:

    ```powershell
    pip freeze > requirements.txt
    ```

4. [optional] Any configuration for the eb extension must be done in the django.config file from the .ebextensions (i.e ladimi/.ebextensions/django.config)

    ```config
    option_settings:
    aws:elasticbeanstalk:container:python:
        WSGIPath: ladimi.wsgi:application
    ```

5. Basic structure should look like this:

    ```
    ~/ladimi/
    |-- .ebextensions
    |   `-- django.config
    |-- ladimi
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    |-- db.sqlite3
    |-- manage.py
    `-- requirements.txt
    ```

6. Initialize the EB CLI:
    ```powershell
    eb init -p python-3.7 django-tutorial
    ```

7. [optional] Configure the key pair for the EC2 instance:

    ```powershell
    # from the Django project folder, execute the below command:
    eb init
    # Then select the options as below:
    ```

    ```
    Do you want to set up SSH for your instances?
    (y/n): y
    Select a keypair.
    1) my-keypair
    2) [ Create new KeyPair ]
    # If you don't see the prompt or need to change your settings later, run **eb init -i**.
    ```

8. Create an environment and deploy your application to it with eb create

    ```powershell
    eb create ladimi-env
    ```

9. When the environment creation process completes, find the domain name of your new environment by running eb status

    ```powershell
    eb status
    ```

    ```
    Environment details for: django-env
    Application name: django-tutorial
    ...
    CNAME: anything-xyz.elasticbeanstalk.com
    ...
    ```

10. Open the settings.py file in the ladimi directory. Locate the ALLOWED_HOSTS setting, and then add your application's domain name that you found in the previous step to the setting's value. If you can't find this setting in the file, add it to a new line.

    ```python
    ALLOWED_HOSTS = ['anything-xyz.elasticbeanstalk.com', 'ladimi.com']
    ```

11. Deploy to EB with the new changes. This command will be used for any updates to the application.

    ```powershell
    eb deploy
    ```

12. Open the website with below command:

    ```powershell
    eb open
    ```

13. Set Route 53 to use your domain.