import base64
import zlib


def main() -> None:
    pob_code = ""
    with open("scripts/temp.txt") as f:
        pob_code = f.read()

    base64_decode = base64.urlsafe_b64decode(pob_code)
    decompressed_xml = zlib.decompress(base64_decode)

    with open("scripts/output.xml", mode="wb") as f:
        f.write(decompressed_xml)


if __name__ == "__main__":
    main()
