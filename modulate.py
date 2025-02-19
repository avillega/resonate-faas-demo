import uuid
from resonate.resonate import Resonate
from resonate.retry_policy import never
from resonate.stores.remote import RemoteStore
from resonate.context import Context
from resonate.task_sources.poller import Poller
from resonate.targets import poll
import argparse

resonate = Resonate(store=RemoteStore(), task_source=Poller(group="entry"))


def get_by_id(id):
    record = resonate.promises.get(id=id)
    if record.is_completed:
        return record.value.data
    return None


@resonate.register()
def execute(ctx: Context, script_content, id): ...


@resonate.register(retry_policy=never())
def detached_rfi(ctx: Context, content, id, machine_type):
    yield ctx.rfi(execute, content, id).options(id=id, send_to=poll("gpu"))
    return


@resonate.register(retry_policy=never())
def prep_execute(ctx: Context, id, script, machine_type, wait):
    try:
        content = ""
        with open(script, "r") as file:
            content = file.read()

        print("Sending script to be executed in gpu")
        if wait:
            result = yield ctx.rfc(execute, content, id).options(
                id=id, send_to=poll("gpu")
            )
            return result
        else:
            detached_id = f"detached_{id}"
            yield ctx.detached(detached_id, detached_rfi, content, id, "gpu")
            return None

    except FileNotFoundError as ef:
        print("Error: File not found.")
        raise ef
    except Exception as e:  # Catch any other exceptions
        print(f"An error occurred: {e}")
        raise e


def main():
    parser = argparse.ArgumentParser(description="Execute a Python script remotely.")
    parser.add_argument(
        "-m",
        "--machine",
        dest="machine_type",
        help="Type of machine to execute on.",
        default="gpu",
    )
    parser.add_argument(
        "-i", "--id", dest="id", help="Sets an id, defaults to a random uuid."
    )
    parser.add_argument(
        "-w",
        "--no-wait",
        dest="wait",
        action="store_false",
        help="Wait for the script to finish.",
    )
    parser.add_argument(
        "-l", "--local", action="store_true", help="Force local execution."
    )
    parser.add_argument("--get", dest="get_id", action="store", help="Which id to get")

    args, argv = parser.parse_known_args()

    if args.get_id is not None:
        res = get_by_id(args.get_id)
        if res:
            print(f"Job results located at: {res}")
        else:
            print(f"Job {args.get_id} is not ready yet.")

        return

    id = args.id
    if args.id is None:
        id = str(uuid.uuid4())

    print(f"You can retrive this execution using {id}")
    if len(argv) < 1:
        print("Script name is required")
        exit(1)

    print(f"Will execute {argv[0]} in {args.machine_type}...")
    handle = prep_execute.run(
        f"execution-{id}-{uuid.uuid4()}", id, argv[0], args.machine_type, args.wait
    )

    result = handle.result()
    if result is not None:
        print(f"results are located at {result}")


if __name__ == "__main__":
    main()
