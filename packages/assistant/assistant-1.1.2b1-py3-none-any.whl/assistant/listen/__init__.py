try:
    import listen
except (ModuleNotFoundError, ImportError) as e:
    print(e)
    print("To speak with Assistant, you need to install the listen module.")
    print("Run the following command:\n```shell\npip install -r stt-listen\n```")
    sys.exit(1)

if __name__ == '__main__':
    from assistant.listen.main import main
    try:
        main()
    except KeyboardInterrupt:
        exit(1)
