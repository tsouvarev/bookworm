from tests.factories import BookFactory


def generate_objects():
    print("Creating books...")
    BookFactory.create_batch(size=10)
    print("Done.")


if __name__ == "__main__":
    # have to import top-level package to initialize mongoengine
    import bookworm  # noqa

    generate_objects()
