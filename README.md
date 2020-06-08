# ladimi-aws

CI/CD Django project to work with Elastic BeanStalk (EB) and AWS CodePipeline.

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

3. If new packages are added, execute the below command from the Django project folder (i.e ladimi), instead of the root folder of the [Git](https://git-scm.com/) repository:

    ```powershell
    pipenv update
    ```

    More information could be found in the [Pipenv: Python Dev Workflow for Humans Page](https://pipenv.pypa.io/en/latest/)

    New Amazon Linux 2 supports pipenv, no more requirements.txt are required.

4. [optional] Any configuration for the eb extension must be done in the django.config file from the .ebextensions (i.e ladimi/.ebextensions/django.config)

    ```yaml
        option_settings:
        aws:elasticbeanstalk:environment:proxy:staticfiles:
            /static: static
            /static/images: static/images
        aws:elasticbeanstalk:container:python:
            WSGIPath: ladimi.wsgi:application

        container_commands:
        collectstatic:
            command: "$PYTHONPATH/python manage.py collectstatic --noinput"
    ```

    We have to set the staticfiles folder in the EB to be able to use them, just is s3 or CDN is not being used. Also, to avoid having to run another command a [container_commands](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers-ec2.html) can be set to collect the statics from Django application or project.

5. Basic structure should look like this:

    ```x
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
    eb init -p python-3.7 ladimi-eb
    ```

7. [optional] Configure the key pair for the EC2 instance:

    ```powershell
    # from the Django project folder, execute the below command:
    eb init
    # Then select the options as below:
    ```

    ```x
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

    ```x
    Environment details for: ladimi-env
    Application name: ladimi-eb
    ...
    CNAME: anything-xyz.elasticbeanstalk.com
    ...
    ```

10. Open the settings.py file in the ladimi directory. Locate the ALLOWED_HOSTS setting, and then add your application's domain name that you found in the previous step to the setting's value. If you cannot find this setting in the file, add it to a new line.

    ```python
    ALLOWED_HOSTS = ['anything-xyz.elasticbeanstalk.com', 'ladimi.com']
    ```

    _If a domain is owned, then it would be easier to just set the allowed host to that domain, like in the above example_
11. Deploy to EB with the new changes. This command will be used for any updates to the application.

    ```powershell
    eb deploy
    ```

12. Open the website with below command:

    ```powershell
    eb open
    ```

13. Set Route 53 to use your domain.
    - Because EB will create a [load balancer](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-elb-load-balancer.html), it is strongly recommended to set the [record set](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/rrsets-working-with.html) to the load balancer URL, instead of the EB url.

Note: _final structure should look like the below tree:_
