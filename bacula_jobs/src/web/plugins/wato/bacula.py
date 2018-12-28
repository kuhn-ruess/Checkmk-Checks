

group = "agents/" + _("Agent Plugins")
register_rule(group,
    "agent_config:bacula",
    DropdownChoice(
        title = _("Bacula Jobs (Linux)"),
        help = _("The plugin <tt>cula.sh</tt> allows monitoring of Bacula Jobs"),
        choices = [
            ( {},   _("Deploy plugin") ),
            ( None, _("Do not deploy plugin") ),
        ]
    )
)

bacula_job_states = [
    ('A',  "Canceled by user"),
    ('B',  "Blocked"),
    ('C',  "Created, but not running"),
    ('c',  "Waiting for client resource"),
    ('D',  "Verify differences"),
    ('d',  "Waiting for maximum jobs"),
    ('E',  "Terminated in error"),
    ('e',  "Non-fatal error"),
    ('f',  "fatal error"),
    ('F',  "Waiting on File Daemon"),
    ('j',  "Waiting for job resource"),
    ('M',  "Waiting for mount"),
    ('m',  "Waiting for new media"),
    ('p',  "Waiting for higher priority jobs to finish"),
    ('R',  "Running"),
    ('S',  "Scan"),
    ('s',  "Waiting for storage resource"),
    ('T',  "Terminated normally"),
    ('t',  "Waiting for start time"),
]

register_check_parameters(
    subgroup_applications,
    "bacula_jobs",
    _("Bacula Jobs"),
    Dictionary(
        elements = [
            ( "max_age",
                Tuple(
                    title = _("Age of last Backup"),
                    elements = [
                        Age(title=_("Warning at")),
                        Age(title=_("Critical at")),
                    ]
                ),
            ),
            ( "ok_states",
                ListChoice(
                    title = _("States which result in OK"),
                    choices = bacula_job_states,
                    default_value = ['T', 'R']
                    )
            ),
            ( "crit_states",
                ListChoice(
                    title = _("States which result in Critical"),
                    choices = bacula_job_states,
                    default_value = ['E', 'f']
                    )
            ),
        ]
    ),
    TextAscii(
        title = _("Job Name"),
        allow_empty = False
    ),
    'dict'
)

