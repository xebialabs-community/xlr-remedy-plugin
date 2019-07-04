# XL Release Remedy plugin

[![Build Status][xlr-remedy-plugin-travis-image]][xlr-remedy-plugin-travis-url]
[![Codacy Badge][xlr-remedy-plugin-codacy-image]][xlr-remedy-plugin-codacy-url]
[![Codeclimate Badge][xlr-remedy-plugin-codeclimate-image]][xlr-remedy-plugin-codeclimate-url]
[![License: MIT][xlr-remedy-plugin-license-image]][xlr-remedy-plugin-license-url]
![Github All Releases][xlr-remedy-plugin-downloads-image]
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fxebialabs-community%2Fxlr-remedy-plugin.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fxebialabs-community%2Fxlr-remedy-plugin?ref=badge_shield)

[xlr-remedy-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-remedy-plugin.svg?branch=master
[xlr-remedy-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-remedy-plugin
[xlr-remedy-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-remedy-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-remedy-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-remedy-plugin/total.svg
[xlr-remedy-plugin-codacy-image]: https://api.codacy.com/project/badge/Grade/a1923f691301487f8386153fda74565f
[xlr-remedy-plugin-codacy-url]: https://www.codacy.com/app/vlussenburg/xlr-remedy-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-remedy-plugin&amp;utm_campaign=Badge_Grade
[xlr-remedy-plugin-codeclimate-image]: https://api.codeclimate.com/v1/badges/10e8314f66faa46b256e/maintainability
[xlr-remedy-plugin-codeclimate-url]: https://codeclimate.com/github/xebialabs-community/xlr-remedy-plugin/maintainability

## Preface ##

This document describes the functionality provided by the XL Release Remedy plugin. The tasks implemented by this plugin can create, update and query entries on a Remedy Server via the server's REST API.

See the **[XL Release Documentation](https://docs.xebialabs.com/xl-release/)** for background information on XL Release concepts.

## Overview ##

The XL Release Remedy plugin enables you interact with BMC Remedy services.

## Tasks

![checkStatus](images/checkStatus.png)

![createEntry](images/createEntry.png)

![findEntry](images/findEntry.png)

![pollingCheckStatus](images/pollingCheckStatus.png)

![queryEntries](images/queryEntries.png)

![updateEntry](images/updateEntry.png)

## Requirements ##

* **XL Release** 7.x+

## Installation ##

* Download the latest plugin version JAR from the `releases`.
* Follow the guide [here](https://docs.xebialabs.com/xl-release/how-to/install-or-remove-xl-release-plugins.html)

## Testing ##

This plugin comes with a Flask container with a stub for BMC Remedy so it can be tested in isolation. If you run `./gradlew clean runDockerCompose` a XL Release container will be started together with the Stub. There will be a Remedy template loaded that has all tasks set up. These tasks can all run successfully against the stub. Please make sure you update the tests and the code when updating this plugin.


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fxebialabs-community%2Fxlr-remedy-plugin.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fxebialabs-community%2Fxlr-remedy-plugin?ref=badge_large)