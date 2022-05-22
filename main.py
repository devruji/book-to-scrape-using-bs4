from src.framework import flow
"""
This is the main driver of the task. Please import and call the appropriate
functions/objects to get the desired output.
"""


def main():
    '''
        Executor
    '''
    try:
        flow()

    except Exception as e:
        print(e)
    # raise NotImplementedError


if __name__ == '__main__':
    main()
