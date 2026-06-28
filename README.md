# Flask-SecurityTxt

[![release](https://img.shields.io/gitea/v/release/parcifal/flask-security-txt?gitea_url=https%3A%2F%2Fscm.parcifal.dev&label=latest+release)][release]
[![pypi](https://img.shields.io/pypi/v/Flask-SecurityTxt?label=pypi+release)][pypi]
[![develop](https://scm.parcifal.dev/parcifal/flask-security-txt/badges/workflows/push.yml/badge.svg?label=develop&branch=develop)][develop]
[![master](https://scm.parcifal.dev/parcifal/flask-security-txt/badges/workflows/push.yml/badge.svg?label=master&branch=master)][master]
[![gitlab](https://img.shields.io/gitlab/last-commit/parcifal%2Fflask-security-txt?label=gitlab+mirror)][gitlab]
[![github](https://img.shields.io/github/last-commit/parcifal%2Fflask-security-txt?label=github+mirror)][github]

![Flask-SecurityTxt Logo][logo]

Flask-SecurityTxt is a simple extension for Flask that makes it easy to add a 
security.txt file to your website. This file, as specified by the [Internet 
Security Research Group](https://securitytxt.org/), is used to provide 
information to security researchers about how to report vulnerabilities in your 
website.

 > The Flask-SecurityTxt logo makes use of the [`cloud-lock-outline`][lock] 
 > icon created by [Michael Richins][richins] as part of the [Material Design 
 > Icons (MDI) library][mdi] and published through 
 > [Pictogrammers][pictogrammers] under the Apache License 2.0.

## Installation

You can install Flask-SecurityTxt using pip:

```bash
pip install Flask-SecurityTxt
```

## Usage

```python
from flask import Flask
from flask_security_txt import SecurityTxt

app = Flask(__name__)
security_txt = SecurityTxt(app)
```

You can also customize the contents of the security.txt file by providing the
following settings in the configuration file:

| Property                           | Type                | Default                 | Description                                                                                                                                                                                                                                                                                                                    |
|------------------------------------|---------------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `SECURITY_TXT_ENDPOINT`            | `str`               | `"security_txt"`        | The name by which the end-point will be known to the Flask-app.                                                                                                                                                                                                                                                                |
| `WELL_KNOWN_DIR`                   | `str`               | `".well-known"`         | The name of the directory that will contain the security.txt file.                                                                                                                                                                                                                                                             |
| `SECURITY_TXT_FILE_NAME`           | `str`               | `"security.txt"`        | The name of the security.txt file.                                                                                                                                                                                                                                                                                             |
| `SECURITY_TXT_SIGN_KEY`            | `str`               | `None`                  | The path to a file containing a PGP key used for signing the security.txt file.                                                                                                                                                                                                                                                |
| `SECURITY_TXT_CONTACT`             | `str` `Iterable`    | `None`                  | The value of the `Contact` field. An `Iterable` type value will result in multiple `Contact` fields. If `None`, the value is automatically generated from `SECURITY_TXT_CONTACT_MAILBOX`.                                                                                                                                      |
| `SECURITY_TXT_CONTACT_MAILBOX`     | `str`               | `"security"`            | The local part of the automatically generated `Contact` email address. Only used if `SECURITY_TXT_CONTACT` is `None`.                                                                                                                                                                                                          |
| `SECURITY_TXT_EXPIRES`             | `str` `datetime`    | `None`                  | The value of the `Expires` field. A `str` type value is parsed into a `datetime` using `dateutil`; an unparseable string raises a `ValueError`. A `datetime` type value is formatted as an ISO 8601 timestamp with microseconds stripped. If `None`, the value is automatically generated using `SECURITY_TXT_EXPIRES_OFFSET`. |
| `SECURITY_TXT_EXPIRES_OFFSET`      | `tuple` `timedelta` | `(0, 0, 0, 0, 0, 0, 1)` | The offset applied to `datetime.now()` to automatically generate the `Expires` field value. A `tuple` is unpacked and passed to the `timedelta` constructor, which interprets the values as days, seconds, microseconds, milliseconds, minutes, hours, and weeks.                                                              |
| `SECURITY_TXT_ENCRYPTION`          | `str` `Iterable`    | `None`                  | The value of the `Encryption` field. An `Iterable` type value will result in multiple `Encryption` fields. A value of `None` will omit the field entirely.                                                                                                                                                                     |
| `SECURITY_TXT_ACKNOWLEDGEMENTS`    | `str` `Iterable`    | `None`                  | The value of the `Acknowledgments` field. An `Iterable` type value will result in multiple `Acknowledgments` fields. A value of `None` will omit the field entirely.                                                                                                                                                           |
| `SECURITY_TXT_PREFERRED_LANGUAGES` | `str` `Iterable`    | `None`                  | The value of the `Preferred-Languages` field. An `Iterable` type value will result in a comma-separated string. If `None`, the value falls back to the translations listed by the `Flask-Babel` extension if it is loaded, or `"en"` otherwise.                                                                                |
| `SECURITY_TXT_CANONICAL`           | `str`               | `None`                  | The value of the `Canonical` field. If `None`, the value is resolved from the endpoint name in `SECURITY_TXT_ENDPOINT` using `url_for`. A value of `None` with no resolvable endpoint will omit the field.                                                                                                                     |
| `SECURITY_TXT_POLICY`              | `str` `Iterable`    | `None`                  | The value of the `Policy` field. An `Iterable` type value will result in multiple `Policy` fields. A value of `None` will omit the field entirely.                                                                                                                                                                             |
| `SECURITY_TXT_HIRING`              | `str` `Iterable`    | `None`                  | The value of the `Hiring` field. An `Iterable` type value will result in multiple `Hiring` fields. A value of `None` will omit the field entirely.                                                                                                                                                                             |
| `SECURITY_TXT_FIELD_CASE`          | `str`               | `"standard"`            | Controls the casing of field names in the output. Accepted values are `"standard"` (title case, e.g. `Contact:`), `"lower"` (e.g. `contact:`), and `"upper"` (e.g. `CONTACT:`).                                                                                                                                                |
| `SECURITY_TXT_HEADER`              | `str`               | `None`                  | A comment block prepended to the security.txt. Set to `None` to omit the header entirely.                                                                                                                                                                                                                                      |
| `SECURITY_TXT_FOOTER`              | `str`               | <default footer>        | A comment block appended to the security.txt. The default footer includes the Flask-SecurityTxt version and project links. Set to `None` to omit the footer entirely.                                                                                                                                                          |

### Configuring Comments

For each field, a comment can be added on the line immediately preceding it by
setting a config key of the form `SECURITY_TXT_<FIELD>_COMMENT`, where
`<FIELD>` is the upper-case field name (e.g. `SECURITY_TXT_CONTACT_COMMENT`,
`SECURITY_TXT_EXPIRES_COMMENT`). It is up to the developer to prepend each
line of the comment with a `#` and add any desired whitespace.

### Configuring Contact Details

The `Contact` field of the security.txt file can be configured with one of 
two different ways. First of all, the whole value string can be defined
using the `SECURITY_TXT_CONTACT` property. This takes precedence over the
alternative method, which uses the `SECURITY_TXT_CONTACT_MAILBOX` property.
The value of this property is combined with the domain name of the current
host, as it is known to Flask. The latter method is less reliable, as such the
prior method is preferred if possible. By default, the contact is set to be
"security@<domain>", with the domain name being provided by Flask.

## Example

A security.txt file will be available in your website's `.well-known` 
directory, with the following contents:

```text
Contact: mailto:security@example.com
Encryption: https://example.com/key.asc
Canonical: https://example.com/.well-known/security.txt
```

## Contributing

Found a bug? Have a suggestion? Open an issue or submit a merge request at
[the Forgejo repository](https://scm.parcifal.dev/parcifal/flask-security-txt). All 
contributions are welcome.

[logo]: https://scm.parcifal.dev/parcifal/flask-security-txt/raw/branch/master/assets/logo.png

[pictogrammers]: https://pictogrammers.com/
[richins]: https://pictogrammers.com/contributor/MrGrigri/
[lock]: https://pictogrammers.com/library/mdi/icon/cloud-lock-outline/
[mdi]: https://pictogrammers.com/library/mdi/

[license]: https://scm.parcifal.dev/parcifal/flask-security-txt/src/branch/master/LICENSE

[release]: https://scm.parcifal.dev/parcifal/flask-security-txt/releases/latest
[gitlab]: https://gitlab.com/parcifal/flask-security-txt
[github]: https://github.com/parcifal/flask-security-txt
[develop]: https://scm.parcifal.dev/parcifal/flask-security-txt/src/branch/develop
[master]: https://scm.parcifal.dev/parcifal/flask-security-txt/src/branch/master

[pypi]: https://pypi.org/project/Flask-SecurityTxt/