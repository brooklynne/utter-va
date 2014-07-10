## Welcome to Utter.io and StackMonkey!
Hello and welcome. I'm @kordless on HackerNews, Twitter, Gmail, and just about everything else. I spent a bit of extra time writing up as much as I could here so you can quickly digest it now, while at work, and then maybe you'll come play with it later, in your spare time.  I'm work on this 100% of my working hours now and would love to hear from anyone who is interested in helping out with it: I currently need users familiar with OpenStack to test the appliance.

Utter.io is like AirBnb for excess compute: The utter.io project provides fast location and provisioning of compute resources within a cooperative set of systems managed by [OpenStack](http://openstack.org/) operators. Resource accounting inside the network is settled with Bitcoin and purchases of compute instances can be made by users without an account. Additionally, groups of operators can form adhoc hybrid clouds, allowing fast scaling and sharing of excess compute resources between trusted entities.  If you are familiar with cloud terminology/slang, this idea may be one possible solution to some of the challenges in achieving cloud federation.

It is my belief that crypto currency technologies can bring a new knob to the existing cloud offerings: **compute**, **storage**, **network** and now **trust**.  The currency conversations around crypto currencies are definitely interesting, but paying for compute with store trust generated by more compute is just downright sexy.

This peek into the future of commodity compute can be seen by visiting the [StackMonkey compute pool](https://www.stackmonkey.com/). StackMonkey is a demonstrative cooperative intended to be the Wild West of compute pools (given it's the first one) and is intended for use by hackers, crackers, security researchers, devs, do-it-yourselfers, and the communities they form around it.  We're fixin' to find out if it'll work or not.

### Project Components
A set of three Open Source repositories provide the project's functionality: [utter-va](https://github.com/StackMonkey/utter-va), [utter-pool](https://github.com/StackMonkey/utter-pool) and [utter-exchange](https://github.com/StackMonkey/utter-exchange). The utter-va virtual appliance provided by this repository builds an instance which runs on top of an OpenStack cluster. The appliance controls the OpenStack cluster's capabilities, advertises other instances for sale on a central pool controller running utter-pool and launches instances when payments are observed on the [Bitcoin Blockchain](https://en.bitcoin.it/wiki/Block_chain) through callbacks made by [Coinbase](https://coinbase.com/).

The first compute pool is hosted on [AppEngine](https://appspot.com) and runs the [StackMonkey pool](https://www.stackmonkey.com). The expected beta launch date of the StackMonkey pool is no later than **July 31, 2014**.  After launch, individuals will be able to purchase instances for Bitcoin from the site. Please note you will need [register an account](https://www.stackmonkey.com/login/) on StackMonkey if you want to sell instances, but buying them doesn't require one.

The utter-exchange component will be completed at a later date. The exchange will serve as a clearing house for compute put up for sale on the various pool controllers. The exchange will operate as a [DAC](https://en.bitcoin.it/wiki/Distributed_Autonomous_Community_/_Decentralized_Application) once the technologies required to create it have been completed.  You can expect a crypto currency to be launched for the project. Both the currency and compute assets managed by the network will be connected to the crypto markets.

### Requirements
The virtual appliance requires a running OpenStack cluster.  If you don't have an OpenStack cluster already running, fear not!  You may follow the instructions for [Installing OpenStack in 10 Minutes](http://www.stackgeek.com/guides/gettingstarted.html) on the [StackGeek website](http://stackgeek.com/). The guy wears a cowboy hat in the video.

Once you have OpenStack installed, you'll need to create or have the following service accounts available:

  - a [StackMonkey](https://www.stackmonkey.com/login/) account (signup takes 1 minute)
  - a [Coinbase](https://coinbase.com/signup?r=52a9c6bf937ab6453a00001e&utm_campaign=user-referral&src=referral-link) account (signup takes 2 minutes)
  - an [Ngrok](https://ngrok.com/) account (signup takes 1 minute)


### Watch the Video
The [following video](https://vimeo.com/91805503) will step you through installing the virtual appliance on your OpenStack cluster.  If you have any questions about the install, you can head over the the [StackMonkey documentation](https://www.stackmonkey.com/docs/) for a list of resources.

[![OpenStack Video](https://raw.github.com/StackGeek/openstackgeek/master/icehouse/openstack_icehouse.png)](https://vimeo.com/97757352)


### Automated Install
If you've previously followed StackGeek's [Installing OpenStack in 10 Minutes](http://www.stackgeek.com/guides/gettingstarted.html) guide, you can run the appliance install script located in the [Icehouse](https://github.com/StackGeek/openstackgeek/tree/master/icehouse) directory:

    ./openstack_stackmonkey_va.sh

The script automatically creates a user and project for the virtual appliance, sets the security group rules for the project, and then launches the appliance on the OpenStack cluster.  SSH keys are automatically created for accessing the appliance's console and a URL will be spit out at the end for accessing the web UI.  

Once the script completes, you can skip to the configuration section below.

### Manual Install
If you have previously installed OpenStack, you can manually start a virtual appliance from the **Horizon UI**.  Begin by logging into OpenStack with an administrative account and then following these steps:

  - Click on the **Admin** tab to the far left and then click on **Identity Panel..Projects**. To the right, click on the **Create Project** button and then enter a new project name called **stackmonkey** in the name field.  Click on **Create Project** below to create the new project.
  - Back in the **Admin** panel, click on **Users**.  To the right, click on the **Create User** button and then create a new user called **stackmonkey** and set the user's password.  Set the primary project to **stackmonkey** and set role of the new user account to **admin**.
  - Log out of the system and then log back in as the **stackmonkey** user.  You should still see the **Admin** tab to the left and the **StackMonkey** project should be highlighted in the pulldown at the top left.

*Note: The StackMonkey user requires admin access to OpenStack so it can gather the capabilities and current load on the hypervisors.  If you are concerned about this from a security standpoint, you may disable the admin role for the StackMonkey user.*

#### Install an Ubuntu Image
The appliance requires an Ubuntu backed instance. If you don't have an Ubuntu image installed on your OpenStack cluster, follow these steps:

  - Click on the **Admin** tab to the far left and then click on **System Panel..Images**. Click on the **Create Image** button to the top right.
  - Name the image **Ubuntu 14.04LTS** and then paste **[http://goo.gl/u2IBP9](http://goo.gl/u2IBP9)** into the location field.
  - Select the **QCOW2** format in the pulldown and make the image public if you want to share it with other OpenStack users.
  - Click **Create Image** to create the new boot image.

#### Create a Keypair
You need to create a key pair that you can use to access the virtual appliance's command line console.  Follow these steps to create the key:

  - Click on the **Project** tab to the far left and then click on **Compute..Instances**. Click on **Access & Security** and then click on the **Key Pairs** tab at the top.
  - Click **Create Key Pair** and name the key pair **stackmonkey**.  Click **Create Key Pair** to create the key pair.  The private key will be downloaded to your local machine.

You need to move the private key into your **.ssh directory** (or similar for Windows) and then change the permissions on it:

	cd ~/Downloads/
	mv stackmonkey.pem ~/.ssh/
    chmod 600 ~/.ssh/stackmonkey.pem

We'll use the key in a minute to ssh into the appliance for maintenance tasks and viewing logs.

#### Set the Access Rules
The instances being sold by the appliance will need unrestricted access from the Internet if they have publicly accessible addresses. For now, the appliance does not manage the security groups, so you need to open up the default group to allow all access to the instances you will be starting.  Follow these steps to setup your access rules for the appliance:

  - Click on the **Project** tab to the far left and then click on **Compute..Access & Security**. To the right, click on the **Create Security Group** button.  Name the security group **'appliance'**, enter a short description and then click **Create Security Group** to create.
  - Click the **Manage Rules** button to the right in the **appliance** security group row.  Click **Add Rule** and then enter the number **'22'** (ssh) in the port field.  Click **Add**.  Repeat this step and enter the number **'80'** (http) in the port field instead.  Click **Add** again.
  - Click the **Manage Rules** button again, but this time click on the **Rule** pulldown and select **Custom ICPMP Rule**.  Enter the number '-1' in **both** the **Type** and **Code** fields.  Click **Add** to add the rule.

Your **appliance** security group rules should now look like this:

[![OpenStack Video](https://raw.github.com/StackGeek/openstackgeek/master/icehouse/openstack_icehouse.png)](https://vimeo.com/97757352)
  
Now follow these steps to set up the access rules for the instances that will be started on the cluster by the appliance:

  - Click on the **Project** tab to the far left and then click on **Compute..Access & Security**.
  - Click the **Manage Rules** button to the right in the **default** security group row.  
  - Delete any existing rules for the default group by clicking on **Delete Rule** in any of the existing rule's rows.
  - Click **Add Rule** and then select **Custom TCP Rule** from the **Rule** pulldown and **Port Range** from the **Open Port** pulldown.
  - Enter the number **'1'** in the **From Port** field. Enter the number **'65535'** in the **To Port** field. Click **Add**.
  - Repeat the previous two steps, but this time select **Custom UDP Rule** from the **Rule** pulldown.  Enter the same numbers for the range.
  - Click **Add Rule** and then select **Custom ICPMP Rule** from the **Rule** pulldown.  
  - Enter the number **'-1'** in **both** the **Type** and **Code** fields.  Click **Add** to add the rule.

Your **default** security group rules should now look like this:

[![OpenStack Video](https://raw.github.com/StackGeek/openstackgeek/master/icehouse/openstack_icehouse.png)](https://vimeo.com/97757352)

#### Start the Instance
Finally, you can start the instance:

  - Click on the **Project** tab to the far left and then click on **Compute..Instances**. To the right, click on the **Create Instance** button.  The create instance dialog should appear.
  - Name the instance **StackMonkey VA** and then click on **Boot From** and select the Ubuntu image you just installed.

Finally, you'll need to enter the following script in the post creation field:

    #cloud-config
    hostname: stackmonkey-va
    manage_etc_hosts: true
    runcmd:
     - [ wget, "http://goo.gl/KJH5Sa", -O, /tmp/install.sh ]
     - chmod 755 /tmp/install.sh
     - /tmp/install.sh

Click on the **Launch Instance** button to launch the appliance.  You can monitor the instance's build state by refreshing the console log.

### Configuration
Once the instance has been started you can access the appliance's UI by entering something like the following into your browser:

    http://10.0.47.2/


#### Shell Access
You can login to the appliance via ssh by using the key you created earlier.  Enter the following to ssh into the instance, assuming your appliance is running at 10.0.47.2 and you named the ssh key stackmonkey:

    ssh -i ~/.ssh/stackmonkey-pem ubuntu@10.0.47.2

Once you are logged in, you can access the command line client's help by changing directories and running the manage app:

    cd /var/www/utterio/
    ./manage.py --help
    

#### Admin Account
Start by creating an administrator account.  Enter the username and password (twice) to use for the admin account and then click the **Create Admin Account** button to create the account.

![Create an admin account.](https://raw.githubusercontent.com/StackMonkey/utter-va/master/webapp/static/img/photo.png)

Note: If you lose the login information to the appliance, you can use the command line to reset the admin account:

     ./manage.py admin -f true


### Security
From a security standpoint, the system management portions of the project should be reasonably secure against bad actors.  It's also reasonable to expect there are holes in that logic. Here is a short list of security features that have been built into the system:

  - Pool controllers use Google federated auth, store no passwords and provide two factor authentication.
  - The pool DOES NOT know about or store credentials related to an appliance's SSL tunnel or Coinbase account.
  - The  appliance's Coinbase API tokens use method level permissions and are suppose to be set to address creation only.
  - SSL tunnels are provided by the Open Source based Ngrok service at [https://ngrok.com/](https://ngrok.com/).
  - SSL tunnels DO NOT relay or store information related to logins, pool tokens or Coinbase credentials.
  - Bitcoin payment callbacks are handled exclusively between the appliance and Coinbase using tokens.
  - Instances can only be started by callbacks from Coinbase to the appliance carrying those coin specific tokens.
  - Custom callback addresses can be used to slightly increase anonymization when provisioning servers for users.
  - Private appliance groups provide a way to leverage trust between entities helping keep bad actors off your appliances.

Obviously, certain aspects of system security can be adversely affected when considering the fact strangers are providing infrastructure services to other strangers.  Weird shit is going to happen, and is expected on the StackMonkey pool.  If you don't like the idea of that, then don't use it.

To mitigate harm to the system and users, the plan is allow the community to provide security services for itself. White lists, black lists, voting buttons, voting addresses, karma on payment addresses, bitcoin contracted bounties, and anything and everything we need to do to ensure we get a good night's rest will be explored and tested. Expect data feeds of all server starts or callbacks, ask prices, bids, URLs used for boots, and general appliance statistics.  All this data can (and will)be used in an open and transparent way to provide reliable and trustworthy infrastructure.

Remember, infrastructure is meant to be [open and transparent](http://www.stackgeek.com/blog/kordless/post/a-code-of-trust). This project makes that a priority.

### Development
If you are doing development on this project, touch a file named **DEV** in the root directory to turn on the development debug configuration:

	cd ~/code/utterio/utter-va/
    touch DEV

If you are doing development on the project, you can start either the single threaded Flask server, or a Gunicorn multithreaded server.  Use the **--gunicorn** flag to start the Gunicorn server:

    ./manage.py serve --gunicorn true

The Gunicorn server will need to be manually restarted to reload certain files and logs to the **logs** directory.

In addition to manually starting the web server, you'll also need to do manual starts of the Ngrok tunnel during dev:

    ngrok -config tunnel.conf start utterio

If you are doing dev or testing on the appliance, you are more than welcome to join the [developer discussion channel](https://gitter.im/StackMonkey/utter-va) on Gitter.  It's likely we're going to need your assistance sooner than later.

I appreciate you being here!

K