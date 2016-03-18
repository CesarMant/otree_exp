import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'otree'

# don't share this with anybody.
# Change this to something unique (e.g. mash your keyboard),
# and then delete this comment.
SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzz'

PAGE_FOOTER = ''

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# ACCESS_CODE_FOR_DEFAULT_SESSION:
# If you have a "default session" set,
# then an access code will be appended to the URL for authentication.
# You can change this as frequently as you'd like,
# to prevent unauthorized server access.

ACCESS_CODE_FOR_DEFAULT_SESSION = 'my_access_code'

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'CNY'
USE_POINTS = True


# e.g. en-gb, de-de, it-it, fr-fr, zh-cn, zh-hans.
# see: https://docs.djangoproject.com/en/1.6/topics/i18n/
#LANGUAGE_CODE = 'zh-cn'
LANGUAGE_CODE = 'en-gb'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = []

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        qualification.LocaleRequirement("EqualTo", "US"),
        qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        #qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.4,
    'participation_fee': 40.00,
    'num_bots': 12,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}


SESSION_CONFIGS = [
    {
        'name': 'pgfield_only',
        'display_name': "Public Goods Game with Punishment (four players/no matching)",
        'num_demo_participants': 4,
        'app_sequence': ['pgfield_only'],
    },
    {
        'name': 'pgfield_only_ch',
        'display_name': "Public Goods Game with Punishment (in Chinese)",
        'num_demo_participants': 12,
        'app_sequence': ['pgfield_only_ch'],
    },
        {
        'name': 'trustfield',
        'display_name': "Trust Game",
        'num_demo_participants': 12,
        'app_sequence': ['trustfield'],
    },
            {
        'name': 'trustfield_ch',
        'display_name': "Trust Game (in Chinese)",
        'num_demo_participants': 12,
        'app_sequence': ['trustfield_ch'],
    },
        {
        'name': 'full_game',
        'display_name': "Full game: Trust Game + Public Goods Game",
        'num_demo_participants': 12,
        'app_sequence': ['trustfield','pgfield','final_results'],
    },
            {
        'name': 'full_game_ch',
        'display_name': "Full game: Trust Game + Public Goods Game (in Chinese)",
        'num_demo_participants': 12,
        'app_sequence': ['trustfield_ch','pgfield_ch','final_results_ch'],
    },
            {
        'name': 'questionnaire',
        'display_name': "Post-experimental questionnaire",
        'num_demo_participants': 1,
        'app_sequence': ['questionnaire'],
    },
            {
        'name': 'trust_2p',
        'display_name': "Trust Game (two players/no matching)",
        'num_demo_participants': 2,
        'app_sequence': ['trust_2p'],
    }
]    


otree.settings.augment_settings(globals())
