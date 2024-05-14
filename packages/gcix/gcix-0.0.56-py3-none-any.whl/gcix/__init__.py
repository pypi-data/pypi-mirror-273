'''
# gcix - Write your GitLab CI pipelines in X languages

[![Apache License 2.0](https://img.shields.io/gitlab/license/gcix%2Fgcix)](https://gitlab.com/gcix/gcix/-/blob/main/LICENSE)

[![GitLab tag (self-managed)](https://img.shields.io/gitlab/v/tag/gcix%2Fgcix?logo=git&color=bright%20green)
](https://gitlab.com/gcix/gcix/-/tags)
[![GitLab pipeline status](https://img.shields.io/gitlab/pipeline-status/gcix%2Fgcix?logo=gitlab)
](https://gitlab.com/gcix/gcix/-/pipelines)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/Gcix%2Fgcix?logo=git)](https://gitlab.com/gcix/gcix/-/commits/main/)
[![GitLab contributors](https://img.shields.io/gitlab/contributors/gcix%2Fgcix?logo=git&color=bright%20green)](https://gitlab.com/gcix/gcix)

[![PyPI - Downloads](https://img.shields.io/pypi/dm/gcix?label=PyPI%20Downloads&logo=python&color=blue)](https://pypi.org/project/gcix/)
[![npm - Downloads](https://img.shields.io/npm/dm/%40gcix/gcix?label=NPM%20downloads&color=blue)](https://www.npmjs.com/package/@gcix/gcix)
[![Docker Pulls](https://img.shields.io/docker/pulls/gcix/gcix?label=Docker%20Pulls&logo=docker&color=blue)](https://hub.docker.com/r/gcix/gcix)

![Matrix](https://img.shields.io/matrix/gcix%3Amatrix.org?logo=matrix&label=Matrix)

The complete documentation is found at [https://docs.gcix.dev](https://docs.gcix.dev)

The GitLab CI X Library (*gcix*) is a library to create dynamic pipelines for GitLab CI.

With the *gcix* you can write your GitLab CI pipelines in multiple languages.

## Supported languages

* Typescript/JavaScript (**native**)
* Python

**A simple pipeline could look like...**

...this in **Typescript**

```python
import { Pipeline, Job } from "gcix"

const pipeline = new Pipeline()
const job = new Job({stage: "build", scripts: ["docker build ."]})

pipeline.addChildren({jobsOrJobCollections: [job]})
pipeline.writeYaml()
```

...this in **Python**

```python
from gcip import Pipeline, Job

pipeline = Pipeline()
job      = Job(stage="build", scripts=["docker build ."])

pipeline.add_children(jobs_or_job_collections=[job])
pipeline.write_yaml()
```

## Intro

The *gcix* is a rewrite of the *gcip*, the reason behind the rewrite is, that I wanted to learn Typescript, and give
developers the choice to use the language they are familiar with. This is because I chose Typescript and a tool called [jsii](https://aws.github.io/jsii/) made by [AWS](https://aws.amazon.com/de/).
*jsii* translates the different language API's to typescript. The user which uses Python is using Pythons syntax, behind the scenes they are getting
translated to Typescript.

### Examples

For a more complex and real world example, just check out our projects [.gitlab-ci.ts](https://gitlab.com/gcix/gcix/-/blob/main/.gitlab-ci.ts). The [.gitlab-ci.ts](https://gitlab.com/gcix/gcix/-/blob/main/.gitlab-ci.ts) is the written example of a working *gcix* in Typescript. The Typescript code is getting rendered and stored as an artifact in the pipeline see [generated yaml file](https://gitlab.com/gcix/gcix/-/jobs/artifacts/main/browse?job=generate-pipeline).

The *gcix* is using the GitLab feature of [dynamic child pipelines](https://docs.gitlab.com/ee/ci/parent_child_pipelines.html#dynamic-child-pipelines). First the `.gitlab-ci.ts` generates the common GitLab CI yaml file which is then started as child pipeline. To get the generated pipeline it is necessary to invoke the `.gitlab-ci.ts` with `ts-node`. To get an idea of a [dynamic child pipelines](https://docs.gitlab.com/ee/ci/parent_child_pipelines.html#dynamic-child-pipelines) setup, you can have a look into [.gitlab-ci.yml](https://gitlab.com/gcix/gcix/-/blob/main/.gitlab-ci.yml).

Creating your pipelines in [any supported programming language](#supported-languages) code allows you all the features of that language, like:

* re-use code (DRY - Don't repeat yourself)
* use variables, control flow (if-then-else, loops, ...), complex data structures, input/output, error handling, ...
* programming paradigms like object-oriented or functional programming
* use 3rd party libraries in your pipelines
* test driven development of pipelines with Jest(Typescript), pytest(Python)...
* package management and distribution of your pipeline code
* ... anything you can imagine to do with Python code

## Documentation

Please read the [User Documentation](https://docs.gcix.dev) to get a quick introduction into most
features of the *gcix*.

You can consult the [API Reference](https://docs.gcix.dev/api/) to get an overview of all classes and methods
and a deeper view into their parameters.

For more information on how to create your own library based on *gcix*, please read the [Developer Documentation](https://docs.gcix.dev/developer/)
to learn about good practices and conventions.

## Why pipelines as code?

There has been a really good discussion on [Hacker News](https://news.ycombinator.com/item?id=26986493#26988105) about *configuration vs code*.
Comments stating that when struggling around with the limitations of static configuration we start writing pipelines as code, until we hassle
around with complex code and start re-writing complex pipelines in static configuration and so forth.

It is absolutely right that pipelines as code are not new and have lots of drawbacks. Chances are good that you have the one guru in you company
loving this project and is writing weird pipelines that nobody else understands. Also comments state that pipelines are those basic things that
build and test your code and shouldn't be in code too, because then you might have a pipeline that build and test your pipeline code.

All those statements are quite true. However all those statements could be applied to static configuration. We started this project because of
GitLab CI yaml files growing over thousands of lines. We tried to implement some logic with clunky rule sets. We tried to re-use code with yaml templates.
We tried to write predefined pipelines by using includes. We started to write bash scripts that do bulk loads of work within a job. All in all
those felt like a bad workaround, while having in mind how much cleaner this might be, writing our pipelines in code. That is why we started
this project and since using it with great success.

However it is absolutely important to understand the *gcix* as a supplement and not as a substitution to GitLab CI yaml files. As long you are fine
with having a couple of jobs you could easily describe in static configuration, just do it. If you feel that you can't manage the complexity of
you static yaml configuration and started to build lots of helper scripts, you could consider writing your pipelines in code. This considerations
should include, if the pipeline code you write is definitely an advantage over the static scripts you had before - and not just for you but also
for your colleagues and the company you are writing the code for.

The *gcix* should be a choice - not a standard.

## Thanks

First of all, I have to thank [**Thomas Steinbach**](https://gitlab.com/thomassteinbach) he created the [GitLab CI Python Library (gcip)](https://gitlab.com/dbsystel/gitlab-ci-python-library) and started a great journey with GitLab CI pipelines as code.
Another thank you goes to the [DB Systel GmbH](https://www.dbsystel.de/).

## Author

*gcix* was created by [Daniel von Eßen](https://gitlab.com/dvonessen) in 2023.

## License

The content of this repository is licensed under the [Apache 2.0 license](http://www.apache.org/licenses/LICENSE-2.0).

Copyright [Daniel von Eßen](https://gitlab.com/dvonessen)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *


@jsii.data_type(
    jsii_type="@gcix/gcix.AddChildrenProps",
    jsii_struct_bases=[],
    name_mapping={
        "jobs_or_job_collections": "jobsOrJobCollections",
        "name": "name",
        "stage": "stage",
    },
)
class AddChildrenProps:
    def __init__(
        self,
        *,
        jobs_or_job_collections: typing.Sequence[typing.Union["Job", "JobCollection"]],
        name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param jobs_or_job_collections: 
        :param name: 
        :param stage: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df60c334bb3349c666a96c0b9eb0a0fd10bedfe170f49913f799b055d493ec1f)
            check_type(argname="argument jobs_or_job_collections", value=jobs_or_job_collections, expected_type=type_hints["jobs_or_job_collections"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "jobs_or_job_collections": jobs_or_job_collections,
        }
        if name is not None:
            self._values["name"] = name
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def jobs_or_job_collections(
        self,
    ) -> typing.List[typing.Union["Job", "JobCollection"]]:
        result = self._values.get("jobs_or_job_collections")
        assert result is not None, "Required property 'jobs_or_job_collections' is missing"
        return typing.cast(typing.List[typing.Union["Job", "JobCollection"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddChildrenProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.ArtifactsProps",
    jsii_struct_bases=[],
    name_mapping={
        "excludes": "excludes",
        "expire_in": "expireIn",
        "expose_as": "exposeAs",
        "name": "name",
        "paths": "paths",
        "public": "public",
        "reports": "reports",
        "untracked": "untracked",
        "when": "when",
    },
)
class ArtifactsProps:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        expire_in: typing.Optional[builtins.str] = None,
        expose_as: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        public: typing.Optional[builtins.bool] = None,
        reports: typing.Optional[typing.Sequence[typing.Union["ArtifactsReport", typing.Dict[builtins.str, typing.Any]]]] = None,
        untracked: typing.Optional[builtins.bool] = None,
        when: typing.Optional["WhenStatement"] = None,
    ) -> None:
        '''
        :param excludes: Paths that prevent files from being added to an artifacts archive.
        :param expire_in: How long the artifacts will be saved before it gets deleted.
        :param expose_as: Used to expose artifacts in merge requests.
        :param name: Name of the artifacts archive. Internally defaults to {PredefinedVariables.ciJobName}-{PredefinedVariables.ciCommitRefSlug}.
        :param paths: Paths relative to project directory ``$CI_PROJECT_DIR``, found files will be used to create the artifacts.
        :param public: True makes artifacts public.
        :param reports: Reports must be a valid dictionary, the key represents a ArtifactsReport and the value must be a valid relativ file path to the reports file.
        :param untracked: If true adds all untracked file to artifacts archive.
        :param when: When to upload artifacts, Only ``on_success``, ``on_failure`` or ``always`` is allowed.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f626d293a27ed91c78507cb1db1ee62396670f50e62b9f2c7edaa3b96329be1a)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument expire_in", value=expire_in, expected_type=type_hints["expire_in"])
            check_type(argname="argument expose_as", value=expose_as, expected_type=type_hints["expose_as"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
            check_type(argname="argument reports", value=reports, expected_type=type_hints["reports"])
            check_type(argname="argument untracked", value=untracked, expected_type=type_hints["untracked"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if expire_in is not None:
            self._values["expire_in"] = expire_in
        if expose_as is not None:
            self._values["expose_as"] = expose_as
        if name is not None:
            self._values["name"] = name
        if paths is not None:
            self._values["paths"] = paths
        if public is not None:
            self._values["public"] = public
        if reports is not None:
            self._values["reports"] = reports
        if untracked is not None:
            self._values["untracked"] = untracked
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Paths that prevent files from being added to an artifacts archive.'''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def expire_in(self) -> typing.Optional[builtins.str]:
        '''How long the artifacts will be saved before it gets deleted.'''
        result = self._values.get("expire_in")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expose_as(self) -> typing.Optional[builtins.str]:
        '''Used to expose artifacts in merge requests.'''
        result = self._values.get("expose_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the artifacts archive.

        Internally defaults to {PredefinedVariables.ciJobName}-{PredefinedVariables.ciCommitRefSlug}.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Paths relative to project directory ``$CI_PROJECT_DIR``, found files will be used to create the artifacts.'''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def public(self) -> typing.Optional[builtins.bool]:
        '''True makes artifacts public.'''
        result = self._values.get("public")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reports(self) -> typing.Optional[typing.List["ArtifactsReport"]]:
        '''Reports must be a valid dictionary, the key represents a ArtifactsReport and the value must be a valid relativ file path to the reports file.'''
        result = self._values.get("reports")
        return typing.cast(typing.Optional[typing.List["ArtifactsReport"]], result)

    @builtins.property
    def untracked(self) -> typing.Optional[builtins.bool]:
        '''If true adds all untracked file to artifacts archive.'''
        result = self._values.get("untracked")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def when(self) -> typing.Optional["WhenStatement"]:
        '''When to upload artifacts, Only ``on_success``, ``on_failure`` or ``always`` is allowed.'''
        result = self._values.get("when")
        return typing.cast(typing.Optional["WhenStatement"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.ArtifactsReport",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "report_type": "reportType"},
)
class ArtifactsReport:
    def __init__(self, *, file: builtins.str, report_type: builtins.str) -> None:
        '''
        :param file: Relative path withing the project, where to find the generated report file.
        :param report_type: https://docs.gitlab.com/ee/ci/yaml/artifacts_reports.html ArtifactsReport type to use.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e50db0ecd289671e1aea241660ca1fde603d026802a5373182b4954af283cec7)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument report_type", value=report_type, expected_type=type_hints["report_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file": file,
            "report_type": report_type,
        }

    @builtins.property
    def file(self) -> builtins.str:
        '''Relative path withing the project, where to find the generated report file.'''
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def report_type(self) -> builtins.str:
        '''https://docs.gitlab.com/ee/ci/yaml/artifacts_reports.html ArtifactsReport type to use.'''
        result = self._values.get("report_type")
        assert result is not None, "Required property 'report_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactsReport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.CacheKeyProps",
    jsii_struct_bases=[],
    name_mapping={"files": "files", "key": "key", "prefix": "prefix"},
)
class CacheKeyProps:
    def __init__(
        self,
        *,
        files: typing.Optional[typing.Sequence[builtins.str]] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param files: 
        :param key: Default: gcix.PredefinedVariables.ciCommitRefSlug
        :param prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55fe4c35d97b905706af6ab04c98d2856dcbde83ceb7f14ee2dee01194eb6327)
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if files is not None:
            self._values["files"] = files
        if key is not None:
            self._values["key"] = key
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def files(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :description:

        A set of files is another way to define a caches unique id.
        Jobs referencing caches with the same set of files are sharing the cache
        contents.

        The `cache:key:files <https://docs.gitlab.com/ee/ci/yaml/#cachekeyfiles>`_
        keyword extends the cache:key functionality by making it easier to reuse
        some caches, and rebuild them less often, which speeds up subsequent
        pipeline runs. Mutually exclusive with ``keys``.
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :default: gcix.PredefinedVariables.ciCommitRefSlug

        :description:

        The key is the unique id of the cache. ``gcix.Job``s
        referencing caches with the same key are sharing the cache contents.
        Mutually exclusive with ``files``
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''
        :description:

        prefixed given ``files`` to allow creation of caches
        for branches.
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CacheKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@gcix/gcix.CachePolicy")
class CachePolicy(enum.Enum):
    '''This enum represents the `cache:policy <https://docs.gitlab.com/ee/ci/yaml/#cachepolicy>`_ keyword. The policy determines if a Job can modify the cache or read him only.'''

    PULLPUSH = "PULLPUSH"
    '''The default behavior of a caching job is to download the files at the start of execution and re-upload them at the end.

    This behavior ensures
    that any changes made by the job are persisted for future runs.
    '''
    PULL = "PULL"
    '''If you are certain that the job does not modify the cached files, you can specify this policy to skip the upload step.

    By setting this policy,
    the job will only download the cached files at the start of execution
    without re-uploading them at the end.
    '''


@jsii.data_type(
    jsii_type="@gcix/gcix.CacheProps",
    jsii_struct_bases=[],
    name_mapping={
        "paths": "paths",
        "cache_key": "cacheKey",
        "policy": "policy",
        "untracked": "untracked",
        "when": "when",
    },
)
class CacheProps:
    def __init__(
        self,
        *,
        paths: typing.Sequence[builtins.str],
        cache_key: typing.Optional["CacheKey"] = None,
        policy: typing.Optional[CachePolicy] = None,
        untracked: typing.Optional[builtins.bool] = None,
        when: typing.Optional["WhenStatement"] = None,
    ) -> None:
        '''
        :param paths: 
        :param cache_key: Default: to ``CacheKey`` with default arguments.
        :param policy: 
        :param untracked: Set the `untracked keyword <https://docs.gitlab.com/ee/ci/yaml/#cacheuntracked>`_ to ``True`` to cache all files that are untracked in your Git repository.
        :param when: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a2924781897361b6f1944ca54c776e0cb84ef97befcf405999f1f3e24fe342)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument cache_key", value=cache_key, expected_type=type_hints["cache_key"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument untracked", value=untracked, expected_type=type_hints["untracked"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "paths": paths,
        }
        if cache_key is not None:
            self._values["cache_key"] = cache_key
        if policy is not None:
            self._values["policy"] = policy
        if untracked is not None:
            self._values["untracked"] = untracked
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''
        :description:

        Use the `paths directive <https://docs.gitlab.com/ee/ci/yaml/#cachepaths>`_
        to choose which files or directories to cache.
        '''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cache_key(self) -> typing.Optional["CacheKey"]:
        '''
        :default: to ``CacheKey`` with default arguments.

        :description: The key keyword defines the affinity of caching between jobs.
        '''
        result = self._values.get("cache_key")
        return typing.cast(typing.Optional["CacheKey"], result)

    @builtins.property
    def policy(self) -> typing.Optional[CachePolicy]:
        '''
        :description:

        The ``CachePolicy`` determines if a Job can modify the cache
        or read him only.
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[CachePolicy], result)

    @builtins.property
    def untracked(self) -> typing.Optional[builtins.bool]:
        '''Set the `untracked keyword <https://docs.gitlab.com/ee/ci/yaml/#cacheuntracked>`_ to ``True`` to cache all files that are untracked in your Git repository.'''
        result = self._values.get("untracked")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def when(self) -> typing.Optional["WhenStatement"]:
        '''
        :description:

        `This keyword <https://docs.gitlab.com/ee/ci/yaml/#cachewhen>`_
        defines when to save the cache, depending on job status.
        Possible values are ``gcix.WhenStatement.ON_SUCCESS``,
        ``gcix.WhenStatement.ON_FAILURE``,
        ``gcix.WhenStatement.ALWAYS``.
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional["WhenStatement"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CacheProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.ChildDict",
    jsii_struct_bases=[],
    name_mapping={"child": "child", "name": "name", "stage": "stage"},
)
class ChildDict:
    def __init__(
        self,
        *,
        child: typing.Union["Job", "JobCollection"],
        name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param child: 
        :param name: 
        :param stage: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ffe8a304fc91b334af5c8ae0a40aa88351b253967dd52f61e50e8f5087b24d)
            check_type(argname="argument child", value=child, expected_type=type_hints["child"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "child": child,
        }
        if name is not None:
            self._values["name"] = name
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def child(self) -> typing.Union["Job", "JobCollection"]:
        result = self._values.get("child")
        assert result is not None, "Required property 'child' is missing"
        return typing.cast(typing.Union["Job", "JobCollection"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChildDict(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@gcix/gcix.IBase")
class IBase(typing_extensions.Protocol):
    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: "IBase") -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: An arbitrary object to compare to.

        :return: boolean
        '''
        ...

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        ...


class _IBaseProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IBase"

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: An arbitrary object to compare to.

        :return: boolean
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b802032a1c461219b94468e0001211e7fa3a98362391007c612b7f50f5be09)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBase).__jsii_proxy_class__ = lambda : _IBaseProxy


@jsii.interface(jsii_type="@gcix/gcix.ICache")
class ICache(IBase, typing_extensions.Protocol):
    pass


class _ICacheProxy(
    jsii.proxy_for(IBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.ICache"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICache).__jsii_proxy_class__ = lambda : _ICacheProxy


@jsii.interface(jsii_type="@gcix/gcix.ICacheKey")
class ICacheKey(IBase, typing_extensions.Protocol):
    pass


class _ICacheKeyProxy(
    jsii.proxy_for(IBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.ICacheKey"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICacheKey).__jsii_proxy_class__ = lambda : _ICacheKeyProxy


@jsii.interface(jsii_type="@gcix/gcix.IImage")
class IImage(typing_extensions.Protocol):
    @jsii.member(jsii_name="withEntrypoint")
    def with_entrypoint(self, entrypoint: typing.Sequence[builtins.str]) -> "Image":
        '''
        :param entrypoint: -

        :description:

        Returns a copy of that image with altered entrypoint.
        You can still use the original Image object with its original entrypoint.
        '''
        ...

    @jsii.member(jsii_name="withTag")
    def with_tag(self, tag: builtins.str) -> "Image":
        '''
        :param tag: -

        :description:

        Returns a copy of that image with altered tag.
        You can still use the original Image object with its original tag.
        '''
        ...


class _IImageProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IImage"

    @jsii.member(jsii_name="withEntrypoint")
    def with_entrypoint(self, entrypoint: typing.Sequence[builtins.str]) -> "Image":
        '''
        :param entrypoint: -

        :description:

        Returns a copy of that image with altered entrypoint.
        You can still use the original Image object with its original entrypoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2a2d3292a09166e2c85abc407e33a4b0b0c26e2917700c4f680d577479fc92)
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
        return typing.cast("Image", jsii.invoke(self, "withEntrypoint", [entrypoint]))

    @jsii.member(jsii_name="withTag")
    def with_tag(self, tag: builtins.str) -> "Image":
        '''
        :param tag: -

        :description:

        Returns a copy of that image with altered tag.
        You can still use the original Image object with its original tag.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb5145e81595053717d524ea935386d483337ec4a56c299aeba9198aa1319f8)
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("Image", jsii.invoke(self, "withTag", [tag]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IImage).__jsii_proxy_class__ = lambda : _IImageProxy


@jsii.interface(jsii_type="@gcix/gcix.IInclude")
class IInclude(IBase, typing_extensions.Protocol):
    '''This module represents the Gitlab CI `Include <https://docs.gitlab.com/ee/ci/yaml/#include>`_ keyword.

    Use include to include external YAML files in your CI/CD configuration.

    `include:local <https://docs.gitlab.com/ee/ci/yaml/#includelocal>`_ example::

       pipeline.addInclude(new IncludeLocal({local: "/templates/.gitlab-ci-template.yml"}))

    `include:file <https://docs.gitlab.com/ee/ci/yaml/#includefile>`_ example::

       pipeline.addInclude(new IncludeFile({
               project="my-group/my-project",
               ref="master",
               file="/templates/.gitlab-ci-template.yml"
           }))

    `include:remote <https://docs.gitlab.com/ee/ci/yaml/#includeremote>`_ example::

       pipeline.addInclude(new IncludeRemote({
                remote: "https://gitlab.com/example-project/-/raw/master/.gitlab-ci.yml"
            }))

    `include:template <https://docs.gitlab.com/ee/ci/yaml/#includetemplate>`_ example::

       pipeline.addInclude(new IncludeTemplate({template: "Auto-DevOps.gitlab-ci.yml"}))

    Special type of include: Use a ``gcix.TriggerJob`` with ``IncludeArtifact``
    to run `a child pipeline with a generated configuration file from a previous job <https://docs.gitlab.com/ee/ci/yaml/README.html#trigger-child-pipeline-with-generated-configuration-file>`_::

       new TriggerJob({includes=[IncludeArtifact(job="generate-config", artifact="generated-config.yml")]})

    :todo:

    Note: The ``IncludeArtifact`` isn't implemented very well as it currently
    cannot handle ``gcix.Job`` objects. You need to know the jobs final name,
    which is not very handy. This could be implemented much better in future.
    '''

    pass


class _IIncludeProxy(
    jsii.proxy_for(IBase), # type: ignore[misc]
):
    '''This module represents the Gitlab CI `Include <https://docs.gitlab.com/ee/ci/yaml/#include>`_ keyword.

    Use include to include external YAML files in your CI/CD configuration.

    `include:local <https://docs.gitlab.com/ee/ci/yaml/#includelocal>`_ example::

       pipeline.addInclude(new IncludeLocal({local: "/templates/.gitlab-ci-template.yml"}))

    `include:file <https://docs.gitlab.com/ee/ci/yaml/#includefile>`_ example::

       pipeline.addInclude(new IncludeFile({
               project="my-group/my-project",
               ref="master",
               file="/templates/.gitlab-ci-template.yml"
           }))

    `include:remote <https://docs.gitlab.com/ee/ci/yaml/#includeremote>`_ example::

       pipeline.addInclude(new IncludeRemote({
                remote: "https://gitlab.com/example-project/-/raw/master/.gitlab-ci.yml"
            }))

    `include:template <https://docs.gitlab.com/ee/ci/yaml/#includetemplate>`_ example::

       pipeline.addInclude(new IncludeTemplate({template: "Auto-DevOps.gitlab-ci.yml"}))

    Special type of include: Use a ``gcix.TriggerJob`` with ``IncludeArtifact``
    to run `a child pipeline with a generated configuration file from a previous job <https://docs.gitlab.com/ee/ci/yaml/README.html#trigger-child-pipeline-with-generated-configuration-file>`_::

       new TriggerJob({includes=[IncludeArtifact(job="generate-config", artifact="generated-config.yml")]})

    :todo:

    Note: The ``IncludeArtifact`` isn't implemented very well as it currently
    cannot handle ``gcix.Job`` objects. You need to know the jobs final name,
    which is not very handy. This could be implemented much better in future.
    '''

    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IInclude"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInclude).__jsii_proxy_class__ = lambda : _IIncludeProxy


@jsii.interface(jsii_type="@gcix/gcix.IIncludeArtifact")
class IIncludeArtifact(IInclude, typing_extensions.Protocol):
    pass


class _IIncludeArtifactProxy(
    jsii.proxy_for(IInclude), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IIncludeArtifact"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIncludeArtifact).__jsii_proxy_class__ = lambda : _IIncludeArtifactProxy


@jsii.interface(jsii_type="@gcix/gcix.IIncludeFile")
class IIncludeFile(IInclude, typing_extensions.Protocol):
    pass


class _IIncludeFileProxy(
    jsii.proxy_for(IInclude), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IIncludeFile"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIncludeFile).__jsii_proxy_class__ = lambda : _IIncludeFileProxy


@jsii.interface(jsii_type="@gcix/gcix.IIncludeLocal")
class IIncludeLocal(IInclude, typing_extensions.Protocol):
    pass


class _IIncludeLocalProxy(
    jsii.proxy_for(IInclude), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IIncludeLocal"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIncludeLocal).__jsii_proxy_class__ = lambda : _IIncludeLocalProxy


@jsii.interface(jsii_type="@gcix/gcix.IIncludeRemote")
class IIncludeRemote(IInclude, typing_extensions.Protocol):
    pass


class _IIncludeRemoteProxy(
    jsii.proxy_for(IInclude), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IIncludeRemote"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIncludeRemote).__jsii_proxy_class__ = lambda : _IIncludeRemoteProxy


@jsii.interface(jsii_type="@gcix/gcix.IIncludeTemplate")
class IIncludeTemplate(IInclude, typing_extensions.Protocol):
    pass


class _IIncludeTemplateProxy(
    jsii.proxy_for(IInclude), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IIncludeTemplate"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIncludeTemplate).__jsii_proxy_class__ = lambda : _IIncludeTemplateProxy


@jsii.interface(jsii_type="@gcix/gcix.IJobBase")
class IJobBase(IBase, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        '''Getter method to receive added tags.'''
        ...

    @jsii.member(jsii_name="addDependencies")
    def add_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", "Need"]],
    ) -> "Job":
        '''
        :param dependencies: -

        :description: Add one or more `dependencies <https://docs.gitlab.com/ee/ci/yaml/README.html#dependencies>`_ to the job.
        '''
        ...

    @jsii.member(jsii_name="addNeeds")
    def add_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", "Need"]],
    ) -> "Job":
        '''
        :param needs: -

        :description: Add one or more `needs <https://docs.gitlab.com/ee/ci/yaml/README.html#needs>`_ to the job.
        '''
        ...

    @jsii.member(jsii_name="addTags")
    def add_tags(self, tags: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param tags: -

        :description: Adds one or more `tags <https://docs.gitlab.com/ee/ci/yaml/README.html#tags>`_ to the job.
        '''
        ...

    @jsii.member(jsii_name="addVariables")
    def add_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "Job":
        '''
        :param variables: -

        :description: Adds one or more `variables <https://docs.gitlab.com/ee/ci/yaml/README.html#variables>`_, to the job.
        '''
        ...

    @jsii.member(jsii_name="appendRules")
    def append_rules(self, rules: typing.Sequence["Rule"]) -> "Job":
        '''
        :param rules: -

        :description: Appends one or more  `rule <https://docs.gitlab.com/ee/ci/yaml/README.html#rules>`_s rules to the job.
        '''
        ...

    @jsii.member(jsii_name="appendScripts")
    def append_scripts(self, scripts: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param scripts: -

        :description: Adds one or more `script <https://docs.gitlab.com/ee/ci/yaml/README.html#script>`_s after the current scripts.
        '''
        ...

    @jsii.member(jsii_name="assignArtifacts")
    def assign_artifacts(self, artifacts: "Artifacts") -> "Job":
        '''
        :param artifacts: -

        :description:

        Sets the `artifacts <https://docs.gitlab.com/ee/ci/yaml/README.html#artifacts>`_ keyword of the Job.
        !! Any previous values will be overwritten.
        '''
        ...

    @jsii.member(jsii_name="assignCache")
    def assign_cache(self, cache: "Cache") -> "Job":
        '''
        :param cache: -

        :description:

        Sets the `cache <https://docs.gitlab.com/ee/ci/yaml/README.html#cache>`_ keyword of the Job.

        !! Any previous values will be overwritten.
        '''
        ...

    @jsii.member(jsii_name="getAllInstanceNames")
    def get_all_instance_names(
        self,
        child: typing.Optional[typing.Union["Job", "JobCollection"]] = None,
    ) -> "OrderedStringSet":
        '''Return all instance names from the given child.

        That means all combinations of the childs name and stage within this
        sequence and all parent sequences.

        :param child: -
        '''
        ...

    @jsii.member(jsii_name="prependRules")
    def prepend_rules(self, rules: typing.Sequence["Rule"]) -> "Job":
        '''
        :param rules: -

        :description: Inserts one or more  `rule <https://docs.gitlab.com/ee/ci/yaml/README.html#rules>`_s before the current rules of the job.
        '''
        ...

    @jsii.member(jsii_name="prependScripts")
    def prepend_scripts(self, scripts: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param scripts: -

        :description: Inserts one or more `script <https://docs.gitlab.com/ee/ci/yaml/README.html#script>`_s before the current scripts.
        '''
        ...


class _IJobBaseProxy(
    jsii.proxy_for(IBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IJobBase"

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        '''Getter method to receive added tags.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @jsii.member(jsii_name="addDependencies")
    def add_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", "Need"]],
    ) -> "Job":
        '''
        :param dependencies: -

        :description: Add one or more `dependencies <https://docs.gitlab.com/ee/ci/yaml/README.html#dependencies>`_ to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8aee6bf51572eeeb275012082671627b86e9490f1dbb1db4c5cb84dd8fa4e52)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("Job", jsii.invoke(self, "addDependencies", [dependencies]))

    @jsii.member(jsii_name="addNeeds")
    def add_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", "Need"]],
    ) -> "Job":
        '''
        :param needs: -

        :description: Add one or more `needs <https://docs.gitlab.com/ee/ci/yaml/README.html#needs>`_ to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e628bdb293dd53db6a2f0816a2ac17bfbee5d4b02ba83bd93fdd6f485e494bc)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("Job", jsii.invoke(self, "addNeeds", [needs]))

    @jsii.member(jsii_name="addTags")
    def add_tags(self, tags: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param tags: -

        :description: Adds one or more `tags <https://docs.gitlab.com/ee/ci/yaml/README.html#tags>`_ to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11c85b5c3830a93f7673707ad357ec8ff0dde3d65439976c2bfb5acaef9d0f2)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("Job", jsii.invoke(self, "addTags", [tags]))

    @jsii.member(jsii_name="addVariables")
    def add_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "Job":
        '''
        :param variables: -

        :description: Adds one or more `variables <https://docs.gitlab.com/ee/ci/yaml/README.html#variables>`_, to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac8f9a4d174a64d5c16c0fe9e19e0e2c7db098410e99d21fc33ad34bd7c324f)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("Job", jsii.invoke(self, "addVariables", [variables]))

    @jsii.member(jsii_name="appendRules")
    def append_rules(self, rules: typing.Sequence["Rule"]) -> "Job":
        '''
        :param rules: -

        :description: Appends one or more  `rule <https://docs.gitlab.com/ee/ci/yaml/README.html#rules>`_s rules to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75844a5c81111f43121da92b1093077b892bc159153efe9908f73f142b4d604)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("Job", jsii.invoke(self, "appendRules", [rules]))

    @jsii.member(jsii_name="appendScripts")
    def append_scripts(self, scripts: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param scripts: -

        :description: Adds one or more `script <https://docs.gitlab.com/ee/ci/yaml/README.html#script>`_s after the current scripts.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f5eeeadc0839ee43fe0900370bda5f6b4d589d8f41959d43c55488525e340e)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        return typing.cast("Job", jsii.invoke(self, "appendScripts", [scripts]))

    @jsii.member(jsii_name="assignArtifacts")
    def assign_artifacts(self, artifacts: "Artifacts") -> "Job":
        '''
        :param artifacts: -

        :description:

        Sets the `artifacts <https://docs.gitlab.com/ee/ci/yaml/README.html#artifacts>`_ keyword of the Job.
        !! Any previous values will be overwritten.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca5f0d4ca99667d89a42ee6c3e5fe148cebda32c2d4ede5ce959b9c23be250c4)
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
        return typing.cast("Job", jsii.invoke(self, "assignArtifacts", [artifacts]))

    @jsii.member(jsii_name="assignCache")
    def assign_cache(self, cache: "Cache") -> "Job":
        '''
        :param cache: -

        :description:

        Sets the `cache <https://docs.gitlab.com/ee/ci/yaml/README.html#cache>`_ keyword of the Job.

        !! Any previous values will be overwritten.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b03c43eafa4deb9248e78940883defec43d04a5628eead3c6c2774d4e504cf7)
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
        return typing.cast("Job", jsii.invoke(self, "assignCache", [cache]))

    @jsii.member(jsii_name="getAllInstanceNames")
    def get_all_instance_names(
        self,
        child: typing.Optional[typing.Union["Job", "JobCollection"]] = None,
    ) -> "OrderedStringSet":
        '''Return all instance names from the given child.

        That means all combinations of the childs name and stage within this
        sequence and all parent sequences.

        :param child: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b1d8712cbbdf0e62e8e7b59ad3dd795707957652047f1c88a2a80afa273e2f)
            check_type(argname="argument child", value=child, expected_type=type_hints["child"])
        return typing.cast("OrderedStringSet", jsii.invoke(self, "getAllInstanceNames", [child]))

    @jsii.member(jsii_name="prependRules")
    def prepend_rules(self, rules: typing.Sequence["Rule"]) -> "Job":
        '''
        :param rules: -

        :description: Inserts one or more  `rule <https://docs.gitlab.com/ee/ci/yaml/README.html#rules>`_s before the current rules of the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd0bb7b0e3d0dcbe8ccf63092df6ac928317aeef53b3ef82004df5eb92b4ad8)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("Job", jsii.invoke(self, "prependRules", [rules]))

    @jsii.member(jsii_name="prependScripts")
    def prepend_scripts(self, scripts: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param scripts: -

        :description: Inserts one or more `script <https://docs.gitlab.com/ee/ci/yaml/README.html#script>`_s before the current scripts.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db2ea334fb58d11a07160912556aac724a6f68bfdc320ee0ba009bccc6e73a6a)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        return typing.cast("Job", jsii.invoke(self, "prependScripts", [scripts]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJobBase).__jsii_proxy_class__ = lambda : _IJobBaseProxy


@jsii.interface(jsii_type="@gcix/gcix.IJobCollectionBase")
class IJobCollectionBase(IBase, typing_extensions.Protocol):
    @jsii.member(jsii_name="addDependencies")
    def add_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", "Need"]],
    ) -> "JobCollection":
        '''
        :param dependencies: -

        :description: Add one or more `dependencies <https://docs.gitlab.com/ee/ci/yaml/README.html#dependencies>`_ to the job.
        '''
        ...

    @jsii.member(jsii_name="addNeeds")
    def add_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", "Need"]],
    ) -> "JobCollection":
        '''
        :param needs: -

        :description: Add one or more `needs <https://docs.gitlab.com/ee/ci/yaml/README.html#needs>`_ to the job.
        '''
        ...

    @jsii.member(jsii_name="addTags")
    def add_tags(self, tags: typing.Sequence[builtins.str]) -> "JobCollection":
        '''
        :param tags: -

        :description: Adds one or more `tags <https://docs.gitlab.com/ee/ci/yaml/README.html#tags>`_ to the job.
        '''
        ...

    @jsii.member(jsii_name="addVariables")
    def add_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "JobCollection":
        '''
        :param variables: -

        :description: Adds one or more `variables <https://docs.gitlab.com/ee/ci/yaml/README.html#variables>`_, to the job.
        '''
        ...

    @jsii.member(jsii_name="appendRules")
    def append_rules(self, rules: typing.Sequence["Rule"]) -> "JobCollection":
        '''
        :param rules: -

        :description: Appends one or more  `rule <https://docs.gitlab.com/ee/ci/yaml/README.html#rules>`_s rules to the job.
        '''
        ...

    @jsii.member(jsii_name="appendScripts")
    def append_scripts(self, scripts: typing.Sequence[builtins.str]) -> "JobCollection":
        '''
        :param scripts: -

        :description: Adds one or more `script <https://docs.gitlab.com/ee/ci/yaml/README.html#script>`_s after the current scripts.
        '''
        ...

    @jsii.member(jsii_name="assignArtifacts")
    def assign_artifacts(self, artifacts: "Artifacts") -> "JobCollection":
        '''
        :param artifacts: -

        :description:

        Sets the `artifacts <https://docs.gitlab.com/ee/ci/yaml/README.html#artifacts>`_ keyword of the Job.
        !! Any previous values will be overwritten.
        '''
        ...

    @jsii.member(jsii_name="assignCache")
    def assign_cache(self, cache: "Cache") -> "JobCollection":
        '''
        :param cache: -

        :description:

        Sets the `cache <https://docs.gitlab.com/ee/ci/yaml/README.html#cache>`_ keyword of the Job.

        !! Any previous values will be overwritten.
        '''
        ...

    @jsii.member(jsii_name="getAllInstanceNames")
    def get_all_instance_names(
        self,
        child: typing.Optional[typing.Union["Job", "JobCollection"]] = None,
    ) -> "OrderedStringSet":
        '''Return all instance names from the given child.

        That means all combinations of the childs name and stage within this
        JobCollection and all parent JobCollection's.

        :param child: -
        '''
        ...

    @jsii.member(jsii_name="prependRules")
    def prepend_rules(self, rules: typing.Sequence["Rule"]) -> "JobCollection":
        '''
        :param rules: -

        :description: Inserts one or more  `rule <https://docs.gitlab.com/ee/ci/yaml/README.html#rules>`_s before the current rules of the job.
        '''
        ...

    @jsii.member(jsii_name="prependScripts")
    def prepend_scripts(
        self,
        scripts: typing.Sequence[builtins.str],
    ) -> "JobCollection":
        '''
        :param scripts: -

        :description: Inserts one or more `script <https://docs.gitlab.com/ee/ci/yaml/README.html#script>`_s before the current scripts.
        '''
        ...


class _IJobCollectionBaseProxy(
    jsii.proxy_for(IBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IJobCollectionBase"

    @jsii.member(jsii_name="addDependencies")
    def add_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", "Need"]],
    ) -> "JobCollection":
        '''
        :param dependencies: -

        :description: Add one or more `dependencies <https://docs.gitlab.com/ee/ci/yaml/README.html#dependencies>`_ to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ed935f54f176dfdc4965e1d7085adc5f78d1a96f54b80cd0099a35eebe2fd6)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("JobCollection", jsii.invoke(self, "addDependencies", [dependencies]))

    @jsii.member(jsii_name="addNeeds")
    def add_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", "Need"]],
    ) -> "JobCollection":
        '''
        :param needs: -

        :description: Add one or more `needs <https://docs.gitlab.com/ee/ci/yaml/README.html#needs>`_ to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9630d892d6f3d4bf0dc8151cf297d433db5836784629f91b76e002d4cefe93e)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("JobCollection", jsii.invoke(self, "addNeeds", [needs]))

    @jsii.member(jsii_name="addTags")
    def add_tags(self, tags: typing.Sequence[builtins.str]) -> "JobCollection":
        '''
        :param tags: -

        :description: Adds one or more `tags <https://docs.gitlab.com/ee/ci/yaml/README.html#tags>`_ to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72eae7b63d66111c68fbdb60f5e300b6e5d13d2e320a9966dc44633911ba244)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("JobCollection", jsii.invoke(self, "addTags", [tags]))

    @jsii.member(jsii_name="addVariables")
    def add_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "JobCollection":
        '''
        :param variables: -

        :description: Adds one or more `variables <https://docs.gitlab.com/ee/ci/yaml/README.html#variables>`_, to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460fd04af2f8d7f9bcdc8eed0a359faf483a92b0d620f98ed09b0d166da5667a)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("JobCollection", jsii.invoke(self, "addVariables", [variables]))

    @jsii.member(jsii_name="appendRules")
    def append_rules(self, rules: typing.Sequence["Rule"]) -> "JobCollection":
        '''
        :param rules: -

        :description: Appends one or more  `rule <https://docs.gitlab.com/ee/ci/yaml/README.html#rules>`_s rules to the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed35c4a51a06708dab9a9e45d1872c1b8093d8e5048d76d15ddd9d8b989f6e1)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("JobCollection", jsii.invoke(self, "appendRules", [rules]))

    @jsii.member(jsii_name="appendScripts")
    def append_scripts(self, scripts: typing.Sequence[builtins.str]) -> "JobCollection":
        '''
        :param scripts: -

        :description: Adds one or more `script <https://docs.gitlab.com/ee/ci/yaml/README.html#script>`_s after the current scripts.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6038da2730c42a2edc87e557f36891028cbd10a4a550eec08abcb16050773e01)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        return typing.cast("JobCollection", jsii.invoke(self, "appendScripts", [scripts]))

    @jsii.member(jsii_name="assignArtifacts")
    def assign_artifacts(self, artifacts: "Artifacts") -> "JobCollection":
        '''
        :param artifacts: -

        :description:

        Sets the `artifacts <https://docs.gitlab.com/ee/ci/yaml/README.html#artifacts>`_ keyword of the Job.
        !! Any previous values will be overwritten.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9811da6c6dc7d5c5fb64242904876c23949d64052c73add9321c01dd27d3fa69)
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
        return typing.cast("JobCollection", jsii.invoke(self, "assignArtifacts", [artifacts]))

    @jsii.member(jsii_name="assignCache")
    def assign_cache(self, cache: "Cache") -> "JobCollection":
        '''
        :param cache: -

        :description:

        Sets the `cache <https://docs.gitlab.com/ee/ci/yaml/README.html#cache>`_ keyword of the Job.

        !! Any previous values will be overwritten.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509908ec5f25755b6cff8829d915602bdc20f223d63af18b0bccc725d86eac53)
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
        return typing.cast("JobCollection", jsii.invoke(self, "assignCache", [cache]))

    @jsii.member(jsii_name="getAllInstanceNames")
    def get_all_instance_names(
        self,
        child: typing.Optional[typing.Union["Job", "JobCollection"]] = None,
    ) -> "OrderedStringSet":
        '''Return all instance names from the given child.

        That means all combinations of the childs name and stage within this
        JobCollection and all parent JobCollection's.

        :param child: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__038e7a4899cf6f020080b690e52525857fa7ee8957a8f91439fe84c60abe678e)
            check_type(argname="argument child", value=child, expected_type=type_hints["child"])
        return typing.cast("OrderedStringSet", jsii.invoke(self, "getAllInstanceNames", [child]))

    @jsii.member(jsii_name="prependRules")
    def prepend_rules(self, rules: typing.Sequence["Rule"]) -> "JobCollection":
        '''
        :param rules: -

        :description: Inserts one or more  `rule <https://docs.gitlab.com/ee/ci/yaml/README.html#rules>`_s before the current rules of the job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7e723df0002afa54736fd55b3faa1a343289181dabae9f5cbc5020608cb200)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("JobCollection", jsii.invoke(self, "prependRules", [rules]))

    @jsii.member(jsii_name="prependScripts")
    def prepend_scripts(
        self,
        scripts: typing.Sequence[builtins.str],
    ) -> "JobCollection":
        '''
        :param scripts: -

        :description: Inserts one or more `script <https://docs.gitlab.com/ee/ci/yaml/README.html#script>`_s before the current scripts.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62dc3a436bac4c95e74e3e70dd16aac82e0750b4966b1da2303aefc39fbb8082)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        return typing.cast("JobCollection", jsii.invoke(self, "prependScripts", [scripts]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJobCollectionBase).__jsii_proxy_class__ = lambda : _IJobCollectionBaseProxy


@jsii.interface(jsii_type="@gcix/gcix.INeed")
class INeed(IBase, typing_extensions.Protocol):
    pass


class _INeedProxy(
    jsii.proxy_for(IBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.INeed"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INeed).__jsii_proxy_class__ = lambda : _INeedProxy


@jsii.interface(jsii_type="@gcix/gcix.IPagesJob")
class IPagesJob(typing_extensions.Protocol):
    @jsii.member(jsii_name="assignStage")
    def assign_stage(self, stage: builtins.str) -> "PagesJob":
        '''Set the name of this jobs stage to a value other than ``pages``.

        :param stage: A valid Gitlab CI Job stage name.
        '''
        ...

    @jsii.member(jsii_name="copy")
    def copy(self) -> "Job":
        '''There should be only one instance of this job, that is why this method does not return a copy of this job but the job itself.'''
        ...

    @jsii.member(jsii_name="extendName")
    def extend_name(self, name: builtins.str) -> None:
        '''The jobs name ``pages`` is fixed and can't be altered.

        :param name: -
        '''
        ...

    @jsii.member(jsii_name="extendStage")
    def extend_stage(self, name: builtins.str) -> None:
        '''The stage name can't be altered from parent sequences.

        :param name: -
        '''
        ...

    @jsii.member(jsii_name="extendStageValue")
    def extend_stage_value(self, name: builtins.str) -> None:
        '''Extending the name of the stage is not allowed on this Job.

        :param name: -
        '''
        ...


class _IPagesJobProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IPagesJob"

    @jsii.member(jsii_name="assignStage")
    def assign_stage(self, stage: builtins.str) -> "PagesJob":
        '''Set the name of this jobs stage to a value other than ``pages``.

        :param stage: A valid Gitlab CI Job stage name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9188c1787279eb95b2345d9ee3cf9eecc815fdea5f6a96b76b96212a604c4978)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast("PagesJob", jsii.invoke(self, "assignStage", [stage]))

    @jsii.member(jsii_name="copy")
    def copy(self) -> "Job":
        '''There should be only one instance of this job, that is why this method does not return a copy of this job but the job itself.'''
        return typing.cast("Job", jsii.invoke(self, "copy", []))

    @jsii.member(jsii_name="extendName")
    def extend_name(self, name: builtins.str) -> None:
        '''The jobs name ``pages`` is fixed and can't be altered.

        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9062d2c93cff55583c61a62346b43157576f6dd57b8f0d4ee4c8855522f6426d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "extendName", [name]))

    @jsii.member(jsii_name="extendStage")
    def extend_stage(self, name: builtins.str) -> None:
        '''The stage name can't be altered from parent sequences.

        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad1fa047341648a1112b54541286025899a02708f3b36c4bee831091c4b8986d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "extendStage", [name]))

    @jsii.member(jsii_name="extendStageValue")
    def extend_stage_value(self, name: builtins.str) -> None:
        '''Extending the name of the stage is not allowed on this Job.

        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14db9a17126777706c353f7a3903e56d747ff5ca3938a0b80e5ae592c34ef584)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "extendStageValue", [name]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPagesJob).__jsii_proxy_class__ = lambda : _IPagesJobProxy


@jsii.interface(jsii_type="@gcix/gcix.IPipeline")
class IPipeline(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(self) -> typing.List["Include"]:
        ...

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> typing.List["Service"]:
        ...

    @jsii.member(jsii_name="addInclude")
    def add_include(self, include: "Include") -> "Pipeline":
        '''Let you add global ``gcix.Include``s to the pipeline. `Gitlab CI Documentation <https://docs.gitlab.com/ee/ci/yaml/#include>`_: *"Use include to include external YAML files in your CI/CD configuration."*.

        :param include: -

        :return: the modified ``Pipeline`` object.
        '''
        ...

    @jsii.member(jsii_name="addServices")
    def add_services(self, services: typing.Sequence["Service"]) -> "Pipeline":
        '''Add one or more ``gcix.Service``s to the pipeline.

        Gitlab CI Documentation: *"The services keyword defines a Docker image
        that runs during a job linked to the Docker image that the image keyword
        defines."*

        :param services: simply use strings to name the services to link to the pipeline. Use objects of the ``gcix.Service`` class for more complex service configurations.

        :return: the modified ``Pipeline`` object.
        '''
        ...

    @jsii.member(jsii_name="writeYaml")
    def write_yaml(self, filename: typing.Optional[builtins.str] = None) -> None:
        '''Create the Gitlab CI YAML file from this pipeline object.

        Use that YAML file to trigger a child pipeline.

        :param filename: the file name of the created yaml file.

        :default: generated-config.yml
        '''
        ...


class _IPipelineProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IPipeline"

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(self) -> typing.List["Include"]:
        return typing.cast(typing.List["Include"], jsii.get(self, "includes"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> typing.List["Service"]:
        return typing.cast(typing.List["Service"], jsii.get(self, "service"))

    @jsii.member(jsii_name="addInclude")
    def add_include(self, include: "Include") -> "Pipeline":
        '''Let you add global ``gcix.Include``s to the pipeline. `Gitlab CI Documentation <https://docs.gitlab.com/ee/ci/yaml/#include>`_: *"Use include to include external YAML files in your CI/CD configuration."*.

        :param include: -

        :return: the modified ``Pipeline`` object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e28fe324efc138161bf4679a2d82b5a90737d2bf5d09571a7ae4814a77b990)
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        return typing.cast("Pipeline", jsii.invoke(self, "addInclude", [include]))

    @jsii.member(jsii_name="addServices")
    def add_services(self, services: typing.Sequence["Service"]) -> "Pipeline":
        '''Add one or more ``gcix.Service``s to the pipeline.

        Gitlab CI Documentation: *"The services keyword defines a Docker image
        that runs during a job linked to the Docker image that the image keyword
        defines."*

        :param services: simply use strings to name the services to link to the pipeline. Use objects of the ``gcix.Service`` class for more complex service configurations.

        :return: the modified ``Pipeline`` object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b779b1ab3d54999ef8df97b55356d16db35549e20c989908d936a6e334e27b)
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
        return typing.cast("Pipeline", jsii.invoke(self, "addServices", [services]))

    @jsii.member(jsii_name="writeYaml")
    def write_yaml(self, filename: typing.Optional[builtins.str] = None) -> None:
        '''Create the Gitlab CI YAML file from this pipeline object.

        Use that YAML file to trigger a child pipeline.

        :param filename: the file name of the created yaml file.

        :default: generated-config.yml
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96c454ab0a3f58392b05e7d80dc3a7df875c37d61c317481c85f54e9bb5f1d7)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        return typing.cast(None, jsii.invoke(self, "writeYaml", [filename]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPipeline).__jsii_proxy_class__ = lambda : _IPipelineProxy


@jsii.interface(jsii_type="@gcix/gcix.IRule")
class IRule(IBase, typing_extensions.Protocol):
    @jsii.member(jsii_name="addVariables")
    def add_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "Rule":
        '''Adds one or more `variables <https://docs.gitlab.com/ee/ci/yaml/README.html#variables>`_, each as keyword argument, to the rule.

        Example::

           rule.addVariables({GREETING: "hello", LANGUAGE: "typescript"})

        :param variables: Each variable would be provided as keyword argument:.

        :return: ``Rule``: The modified ``Rule`` object.
        '''
        ...

    @jsii.member(jsii_name="never")
    def never(self) -> "Rule":
        '''This method is intended to be used for predefined rules.

        For instance you have defined an
        often used rule ``on_master`` whose if statement checks if the pipeline is executed on branch
        ``master``. Then you can either run a job, if on master..::

           myJob.appendRules(onMaster)

        ... or do not run a job if on master..::

           myJob.appendRules(onMaster.never())

        :return: A copy of this rule with the ``when`` attribute set to ``WhenStatement.NEVER``
        '''
        ...


class _IRuleProxy(
    jsii.proxy_for(IBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IRule"

    @jsii.member(jsii_name="addVariables")
    def add_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "Rule":
        '''Adds one or more `variables <https://docs.gitlab.com/ee/ci/yaml/README.html#variables>`_, each as keyword argument, to the rule.

        Example::

           rule.addVariables({GREETING: "hello", LANGUAGE: "typescript"})

        :param variables: Each variable would be provided as keyword argument:.

        :return: ``Rule``: The modified ``Rule`` object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7eb42bf680cbe707b884181d461186d13f501dc27feb2ba28b81c356c041b3)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("Rule", jsii.invoke(self, "addVariables", [variables]))

    @jsii.member(jsii_name="never")
    def never(self) -> "Rule":
        '''This method is intended to be used for predefined rules.

        For instance you have defined an
        often used rule ``on_master`` whose if statement checks if the pipeline is executed on branch
        ``master``. Then you can either run a job, if on master..::

           myJob.appendRules(onMaster)

        ... or do not run a job if on master..::

           myJob.appendRules(onMaster.never())

        :return: A copy of this rule with the ``when`` attribute set to ``WhenStatement.NEVER``
        '''
        return typing.cast("Rule", jsii.invoke(self, "never", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRule).__jsii_proxy_class__ = lambda : _IRuleProxy


@jsii.interface(jsii_type="@gcix/gcix.IService")
class IService(IBase, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        ...


class _IServiceProxy(
    jsii.proxy_for(IBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IService"

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IService).__jsii_proxy_class__ = lambda : _IServiceProxy


@jsii.interface(jsii_type="@gcix/gcix.ITriggerJob")
class ITriggerJob(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> typing.Optional[builtins.str]:
        '''The branch of ``project`` the pipeline should be triggered of.'''
        ...

    @branch.setter
    def branch(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(
        self,
    ) -> typing.Optional[typing.List[typing.Union["IncludeLocal", "IncludeFile", "IncludeRemote", "IncludeTemplate", "IncludeArtifact"]]]:
        '''Include a pipeline to trigger (Parent-child pipeline trigger) Mutually exclusiv with ``project``.'''
        ...

    @includes.setter
    def includes(
        self,
        value: typing.Optional[typing.List[typing.Union["IncludeLocal", "IncludeFile", "IncludeRemote", "IncludeTemplate", "IncludeArtifact"]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> typing.Optional[builtins.str]:
        '''The full name of another Gitlab project to trigger (multi-project pipeline trigger).

        Mutually exclusive with ``includes``.
        '''
        ...

    @project.setter
    def project(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> typing.Optional[builtins.str]:
        '''Determines if the result of this pipeline depends on the triggered downstream pipeline (use ``TriggerStrategy.DEPEND``) or if just "fire and forget" the downstream pipeline (use ``None``).'''
        ...

    @strategy.setter
    def strategy(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ITriggerJobProxy:
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.ITriggerJob"

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> typing.Optional[builtins.str]:
        '''The branch of ``project`` the pipeline should be triggered of.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df4d15435ffe1434f16f5a77ca3067eb6d1e89660e177ea313c1544ea86d39d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value)

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(
        self,
    ) -> typing.Optional[typing.List[typing.Union["IncludeLocal", "IncludeFile", "IncludeRemote", "IncludeTemplate", "IncludeArtifact"]]]:
        '''Include a pipeline to trigger (Parent-child pipeline trigger) Mutually exclusiv with ``project``.'''
        return typing.cast(typing.Optional[typing.List[typing.Union["IncludeLocal", "IncludeFile", "IncludeRemote", "IncludeTemplate", "IncludeArtifact"]]], jsii.get(self, "includes"))

    @includes.setter
    def includes(
        self,
        value: typing.Optional[typing.List[typing.Union["IncludeLocal", "IncludeFile", "IncludeRemote", "IncludeTemplate", "IncludeArtifact"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f688d53e106b53582f0d712821dac997079d1479f6bf480ffdfdad656dad406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includes", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> typing.Optional[builtins.str]:
        '''The full name of another Gitlab project to trigger (multi-project pipeline trigger).

        Mutually exclusive with ``includes``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "project"))

    @project.setter
    def project(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade450b81a48ddc3723f73a18409fa603a8144bd2f94a5803fa1a4f8e103cf8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> typing.Optional[builtins.str]:
        '''Determines if the result of this pipeline depends on the triggered downstream pipeline (use ``TriggerStrategy.DEPEND``) or if just "fire and forget" the downstream pipeline (use ``None``).'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "strategy"))

    @strategy.setter
    def strategy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bdf94dfa91262761d1f8e26436a7f93e4e7c281ce993a5314e8719c31f4743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strategy", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITriggerJob).__jsii_proxy_class__ = lambda : _ITriggerJobProxy


@jsii.implements(IImage, IBase)
class Image(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.Image"):
    def __init__(
        self,
        *,
        name: builtins.str,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param entrypoint: 
        :param tag: 
        '''
        props = ImageProps(name=name, entrypoint=entrypoint, tag=tag)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2a35ee4709de564436ef9700b1deb2e1db70796e4d2420b43443a1863bc095)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @jsii.member(jsii_name="withEntrypoint")
    def with_entrypoint(self, entrypoint: typing.Sequence[builtins.str]) -> "Image":
        '''
        :param entrypoint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e5ec7913b580d4210605bbccf430e902713f76606c23b2dfc862e2567edac2)
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
        return typing.cast("Image", jsii.invoke(self, "withEntrypoint", [entrypoint]))

    @jsii.member(jsii_name="withTag")
    def with_tag(self, tag: builtins.str) -> "Image":
        '''
        :param tag: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2dcff1af5d25512515e4467781177e01397539668630064709b27590be91f0f)
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        return typing.cast("Image", jsii.invoke(self, "withTag", [tag]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f239025515d1dc0e5da1f102c2744bb938dceae0d3e0c4ebe1ff277ce65f352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="entrypoint")
    def entrypoint(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "entrypoint"))

    @entrypoint.setter
    def entrypoint(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2046cb85c036453c62ad247747305bd0672c03185a4794cffe555bfed6590490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entrypoint", value)

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fbdfd006a3101ae02bf08db6032fc7decf3d83dcbe48a1c070dcd32d2b4ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.ImageProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "entrypoint": "entrypoint", "tag": "tag"},
)
class ImageProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param entrypoint: 
        :param tag: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a206b1d7a64271bf19bfa8eec764c2d1ced5779801630b5916ef78d8aca78ec3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :description:

        The fully qualified image name. Could include
        repository and tag as usual.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :description: Overwrites the containers entrypoint.
        '''
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''
        :description: Container image tag in registrie to use.
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInclude)
class Include(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.Include"):
    '''This is just an abstract superclass.

    Please use one of the subclasses:

    - ``IncludeLocal``
    - ``IncludeFile``
    - ``IncludeRemote``
    - ``IncludeTemplate``
    - ``IncludeArtifact``
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34cb8f048535f4cf504557cc2b72021e05a1225d61437bcd7eacab367a3a74b9)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="rendered")
    def rendered(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "rendered"))

    @rendered.setter
    def rendered(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6638cd4c88920fbc055b25b74a83ede6f3f7a1be640dfecacc2ed9655b30be7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rendered", value)


@jsii.implements(IIncludeArtifact)
class IncludeArtifact(
    Include,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.IncludeArtifact",
):
    '''
    :description:

    A special type of include: Use a ``TriggerJob``
    with ``IncludeArtifact`` to run
    `a child pipeline with a generated configuration file from a previous job <https://docs.gitlab.com/ee/ci/yaml/README.html#trigger-child-pipeline-with-generated-configuration-file>`_:
    '''

    def __init__(self, *, artifact: builtins.str, job: builtins.str) -> None:
        '''
        :param artifact: Relative path to the artifact which is produced by ``job``.
        :param job: Job name to include the artifact from.
        '''
        props = IncludeArtifactProps(artifact=artifact, job=job)

        jsii.create(self.__class__, self, [props])


@jsii.data_type(
    jsii_type="@gcix/gcix.IncludeArtifactProps",
    jsii_struct_bases=[],
    name_mapping={"artifact": "artifact", "job": "job"},
)
class IncludeArtifactProps:
    def __init__(self, *, artifact: builtins.str, job: builtins.str) -> None:
        '''
        :param artifact: Relative path to the artifact which is produced by ``job``.
        :param job: Job name to include the artifact from.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe231effbeb59a4e5b310a4bd72c6777c20816c2fae07527972344979aeda40)
            check_type(argname="argument artifact", value=artifact, expected_type=type_hints["artifact"])
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact": artifact,
            "job": job,
        }

    @builtins.property
    def artifact(self) -> builtins.str:
        '''Relative path to the artifact which is produced by ``job``.'''
        result = self._values.get("artifact")
        assert result is not None, "Required property 'artifact' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job(self) -> builtins.str:
        '''Job name to include the artifact from.'''
        result = self._values.get("job")
        assert result is not None, "Required property 'job' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludeArtifactProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIncludeFile)
class IncludeFile(Include, metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.IncludeFile"):
    '''This module represents the Gitlab CI `include:file <https://docs.gitlab.com/ee/ci/yaml/#includefile>`_ keyword.'''

    def __init__(
        self,
        *,
        file: builtins.str,
        project: builtins.str,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: Relative path to the file to include.
        :param project: Project to include the file from.
        :param ref: Project branch to include the file from.
        '''
        props = IncludeFileProps(file=file, project=project, ref=ref)

        jsii.create(self.__class__, self, [props])


@jsii.data_type(
    jsii_type="@gcix/gcix.IncludeFileProps",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "project": "project", "ref": "ref"},
)
class IncludeFileProps:
    def __init__(
        self,
        *,
        file: builtins.str,
        project: builtins.str,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: Relative path to the file to include.
        :param project: Project to include the file from.
        :param ref: Project branch to include the file from.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d092556027df5bc534b1b982f559c3a4239787d8fa1946366627c13d0ab8c0)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file": file,
            "project": project,
        }
        if ref is not None:
            self._values["ref"] = ref

    @builtins.property
    def file(self) -> builtins.str:
        '''Relative path to the file to include.'''
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        '''Project to include the file from.'''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''Project branch to include the file from.'''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludeFileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIncludeLocal)
class IncludeLocal(
    Include,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.IncludeLocal",
):
    '''This module represents the Gitlab CI `include:local <https://docs.gitlab.com/ee/ci/yaml/#includelocal>`_ keyword.'''

    def __init__(self, *, local: builtins.str) -> None:
        '''
        :param local: Relative path to the file within this repository to include.
        '''
        props = IncludeLocalProps(local=local)

        jsii.create(self.__class__, self, [props])


@jsii.data_type(
    jsii_type="@gcix/gcix.IncludeLocalProps",
    jsii_struct_bases=[],
    name_mapping={"local": "local"},
)
class IncludeLocalProps:
    def __init__(self, *, local: builtins.str) -> None:
        '''
        :param local: Relative path to the file within this repository to include.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3dcbd3670d94ab59398ee3faaaa53839dece0252157a37879dff6ef28e1fad4)
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local": local,
        }

    @builtins.property
    def local(self) -> builtins.str:
        '''Relative path to the file within this repository to include.'''
        result = self._values.get("local")
        assert result is not None, "Required property 'local' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludeLocalProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIncludeRemote)
class IncludeRemote(
    Include,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.IncludeRemote",
):
    '''
    :description:

    This module represents the Gitlab CI
    `include:remote <https://docs.gitlab.com/ee/ci/yaml/#includeremote>`_ keyword.
    :throws: Error if ``remote`` is not a valid URL.
    '''

    def __init__(self, *, remote: builtins.str) -> None:
        '''
        :param remote: URL to include the file from.
        '''
        props = IncludeRemoteProps(remote=remote)

        jsii.create(self.__class__, self, [props])


@jsii.data_type(
    jsii_type="@gcix/gcix.IncludeRemoteProps",
    jsii_struct_bases=[],
    name_mapping={"remote": "remote"},
)
class IncludeRemoteProps:
    def __init__(self, *, remote: builtins.str) -> None:
        '''
        :param remote: URL to include the file from.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2928dfd23c62e7a2ed12b3f1f4943bd6ac588e797b2f6bff3e4f2cb665cf4bba)
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote": remote,
        }

    @builtins.property
    def remote(self) -> builtins.str:
        '''URL to include the file from.'''
        result = self._values.get("remote")
        assert result is not None, "Required property 'remote' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludeRemoteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIncludeTemplate)
class IncludeTemplate(
    Include,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.IncludeTemplate",
):
    '''
    :description:

    This class represents the Gitlab CI
    `include:template <https://docs.gitlab.com/ee/ci/yaml/#includetemplate>`_ keyword.
    '''

    def __init__(self, *, template: builtins.str) -> None:
        '''
        :param template: Gitlab template pipeline to include.
        '''
        props = IncludeTemplateProps(template=template)

        jsii.create(self.__class__, self, [props])


@jsii.data_type(
    jsii_type="@gcix/gcix.IncludeTemplateProps",
    jsii_struct_bases=[],
    name_mapping={"template": "template"},
)
class IncludeTemplateProps:
    def __init__(self, *, template: builtins.str) -> None:
        '''
        :param template: Gitlab template pipeline to include.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4efed7ce19a60907db78b31497f8feee1fd1f69e18be3c2e46916185d5d36c)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template": template,
        }

    @builtins.property
    def template(self) -> builtins.str:
        '''Gitlab template pipeline to include.'''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludeTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.JobProps",
    jsii_struct_bases=[],
    name_mapping={
        "scripts": "scripts",
        "allow_failure": "allowFailure",
        "artifacts": "artifacts",
        "cache": "cache",
        "dependencies": "dependencies",
        "image": "image",
        "name": "name",
        "needs": "needs",
        "rules": "rules",
        "stage": "stage",
        "tags": "tags",
        "variables": "variables",
    },
)
class JobProps:
    def __init__(
        self,
        *,
        scripts: typing.Sequence[builtins.str],
        allow_failure: typing.Optional[typing.Union[builtins.bool, typing.Sequence[jsii.Number]]] = None,
        artifacts: typing.Optional["Artifacts"] = None,
        cache: typing.Optional["Cache"] = None,
        dependencies: typing.Optional[typing.Sequence[typing.Union["Job", "JobCollection"]]] = None,
        image: typing.Optional[typing.Union[builtins.str, Image]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[typing.Union["Job", "JobCollection", "Need"]]] = None,
        rules: typing.Optional[typing.Sequence["Rule"]] = None,
        stage: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scripts: 
        :param allow_failure: 
        :param artifacts: 
        :param cache: 
        :param dependencies: 
        :param image: 
        :param name: 
        :param needs: 
        :param rules: 
        :param stage: 
        :param tags: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cbed1928941b7d9ab02facad79a3cc0b1c10eac94f6ea0777578cc97ae2c4a)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scripts": scripts,
        }
        if allow_failure is not None:
            self._values["allow_failure"] = allow_failure
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if cache is not None:
            self._values["cache"] = cache
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if image is not None:
            self._values["image"] = image
        if name is not None:
            self._values["name"] = name
        if needs is not None:
            self._values["needs"] = needs
        if rules is not None:
            self._values["rules"] = rules
        if stage is not None:
            self._values["stage"] = stage
        if tags is not None:
            self._values["tags"] = tags
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def scripts(self) -> typing.List[builtins.str]:
        '''
        :description: The `script(s) <https://docs.gitlab.com/ee/ci/yaml/README.html#script>`_ to be executed.
        '''
        result = self._values.get("scripts")
        assert result is not None, "Required property 'scripts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allow_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, typing.List[jsii.Number]]]:
        '''
        :description: The `allow_failure <https://docs.gitlab.com/ee/ci/yaml/#allow_failure>`_ keyword of the Job.
        '''
        result = self._values.get("allow_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, typing.List[jsii.Number]]], result)

    @builtins.property
    def artifacts(self) -> typing.Optional["Artifacts"]:
        '''
        :TODO: add description
        :description: true
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional["Artifacts"], result)

    @builtins.property
    def cache(self) -> typing.Optional["Cache"]:
        '''
        :TODO: add description
        :description: true
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional["Cache"], result)

    @builtins.property
    def dependencies(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection"]]]:
        '''
        :TODO: add description
        :description: true
        '''
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection"]]], result)

    @builtins.property
    def image(self) -> typing.Optional[typing.Union[builtins.str, Image]]:
        '''
        :TODO: add description
        :description: true
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[typing.Union[builtins.str, Image]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :description:

        The name of the job. In opposite to ``stage`` only the name
        is set and not the stage of the job. If ``name`` is set, than the jobs
        stage has no value, which defaults to the 'test' stage.

        Either ``name`` or ``stage`` must be set.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def needs(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", "Need"]]]:
        '''
        :TODO: add description
        :description: true
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection", "Need"]]], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["Rule"]]:
        '''
        :TODO: add description
        :description: true
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["Rule"]], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''
        :description:

        The name and stage of the job. In opposite to ``name`` also
        the jobs stage will be setup with this value.

        Either ``name`` or ``stage`` must be set.
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :TODO: add description
        :description: true
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :TODO: add description
        :description: true
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INeed)
class Need(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.Need"):
    '''This class represents the Gitlab CI `needs <https://docs.gitlab.com/ee/ci/yaml/#needs>`_ keyword. The ``needs`` key-word adds a possibility to allow out-of-order Gitlab CI jobs. A job which needed another job runs directly after the other job as finished successfully.

    :throws: Error If both ``project`` and ``pipeline`` are set.
    '''

    def __init__(
        self,
        *,
        artifacts: typing.Optional[builtins.bool] = None,
        job: typing.Optional[builtins.str] = None,
        pipeline: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifacts: Default: true
        :param job: Default: undefined but requires ``pipeline`` to be set.
        :param pipeline: Default: undefined which requires ``job`` to be set.
        :param project: Default: undefined
        :param ref: Default: undefined
        '''
        props = NeedProps(
            artifacts=artifacts, job=job, pipeline=pipeline, project=project, ref=ref
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee4b3bd273a1b5cb9a8321ea15f051d48d43d483253502450bbeab70c098bd5)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.

        :return: RenderedNeed
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "artifacts"))

    @artifacts.setter
    def artifacts(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d198d6a7a7b04f4ad8b480ac29f9e68d6bcb4e0de77626ebfda46cfd7b7cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifacts", value)

    @builtins.property
    @jsii.member(jsii_name="job")
    def job(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "job"))

    @job.setter
    def job(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50f041f3ef47b596e0b2ce31821eb03d2ed75d5929d6a8bf5da9238de546e42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "job", value)

    @builtins.property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipeline"))

    @pipeline.setter
    def pipeline(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb0a517c21b40a0ad6c3d47dd8207f97524ef628c60a068dbebbde7307bb52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipeline", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "project"))

    @project.setter
    def project(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13713b719c82daa59c3d732be80bf8e00673ab95b0db7d29fa3fd8cc74ab6a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7e33fc9c788da70e893a43de03c4d4b38c8a62eb1b2b0aed9121326d435a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value)


@jsii.data_type(
    jsii_type="@gcix/gcix.NeedProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifacts": "artifacts",
        "job": "job",
        "pipeline": "pipeline",
        "project": "project",
        "ref": "ref",
    },
)
class NeedProps:
    def __init__(
        self,
        *,
        artifacts: typing.Optional[builtins.bool] = None,
        job: typing.Optional[builtins.str] = None,
        pipeline: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifacts: Default: true
        :param job: Default: undefined but requires ``pipeline`` to be set.
        :param pipeline: Default: undefined which requires ``job`` to be set.
        :param project: Default: undefined
        :param ref: Default: undefined
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a28141c95e97f81e6678f904f2b84cd83cc3a7cbde2b1a0cff6fca30c4da6df7)
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if job is not None:
            self._values["job"] = job
        if pipeline is not None:
            self._values["pipeline"] = pipeline
        if project is not None:
            self._values["project"] = project
        if ref is not None:
            self._values["ref"] = ref

    @builtins.property
    def artifacts(self) -> typing.Optional[builtins.bool]:
        '''
        :default: true

        :description: Download artifacts from the ``job`` to depend on.
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def job(self) -> typing.Optional[builtins.str]:
        '''
        :default: undefined but requires ``pipeline`` to be set.

        :description:

        The name of the job to depend on. Could be left if
        ``pipeline`` is set.
        '''
        result = self._values.get("job")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline(self) -> typing.Optional[builtins.str]:
        '''
        :default: undefined which requires ``job`` to be set.

        :description:

        When ``$CI_PIPELINE_ID`` of another pipeline is provided,
        then artifacts from this pipeline are downloaded.
        When the name of an ``other/project`` is provided, then the status of an
        upstream pipeline is mirrored.
        '''
        result = self._values.get("pipeline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''
        :default: undefined

        :description:

        If the ``job`` resides in another pipeline you have to give
        its project name here.
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''
        :default: undefined

        :description: Branch of the remote project to depend on.
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NeedProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrderedStringSet(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.OrderedStringSet",
):
    '''Represents an ordered set of strings.'''

    def __init__(
        self,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Creates a new OrderedStringSet instance.

        :param values: An optional array of values to initialize the set.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a0e3c2a8d12e3bceb2cac68d625620e2accb5164e2849c102e70b3d23090106)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        jsii.create(self.__class__, self, [values])

    @jsii.member(jsii_name="add")
    def add(
        self,
        value: typing.Union[builtins.str, typing.Sequence[builtins.str]],
    ) -> None:
        '''Adds a value or an array of values to the set.

        :param value: The value(s) to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faeabbcd55ceb46f5b615060a98ee7af2b34f0d181d10d30a069dbae8c7e6462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "add", [value]))

    @jsii.member(jsii_name="clear")
    def clear(self) -> None:
        '''Clears the set, removing all values.'''
        return typing.cast(None, jsii.invoke(self, "clear", []))

    @jsii.member(jsii_name="delete")
    def delete(self, value: builtins.str) -> None:
        '''Deletes a value from the set.

        :param value: The value to delete.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f552f03d9ea9c8fa459a2bdec922969c01935e5028a816b687b00a57d5c93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "delete", [value]))

    @jsii.member(jsii_name="has")
    def has(self, value: builtins.str) -> builtins.bool:
        '''Checks if the set contains a specific value.

        :param value: The value to check.

        :return: A boolean indicating if the set contains the value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96a69145aaef180c6ed4c8a576da17c3ab04002311f011d5268c0dfc4ba918c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.invoke(self, "has", [value]))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        '''Returns the number of values in the set.'''
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        '''Returns an array of values in the set.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))


@jsii.data_type(
    jsii_type="@gcix/gcix.PipelineProps",
    jsii_struct_bases=[],
    name_mapping={"includes": "includes"},
)
class PipelineProps:
    def __init__(
        self,
        *,
        includes: typing.Optional[typing.Sequence[Include]] = None,
    ) -> None:
        '''
        :param includes: You can add global ``gcix.Include``s to the pipeline. `Gitlab CI Documentation <https://docs.gitlab.com/ee/ci/yaml/#include>`_: *"Use include to include external YAML files in your CI/CD configuration."*.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3477f8a77546ea9831987070462144f4c75f5f2d077cd7472f82ca430d8f9b42)
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[Include]]:
        '''You can add global ``gcix.Include``s to the pipeline. `Gitlab CI Documentation <https://docs.gitlab.com/ee/ci/yaml/#include>`_: *"Use include to include external YAML files in your CI/CD configuration."*.'''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[Include]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PredefinedVariables(
    metaclass=jsii.JSIIMeta,
    jsii_type="@gcix/gcix.PredefinedVariables",
):
    '''This class contains constants for `Gitlab CI predefined variables <https://docs.gitlab.com/ee/ci/variables/predefined_variables.html>`_.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="chatChannel")
    def chat_channel(cls) -> builtins.str:
        '''Source chat channel which triggered the ChatOps command.

        Added in GitLab 10.6
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "chatChannel"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="chatInput")
    def chat_input(cls) -> builtins.str:
        '''Additional arguments passed in the ChatOps command.

        Added in GitLab 10.6
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "chatInput"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ci")
    def ci(cls) -> builtins.str:
        '''Mark that job is executed in CI environment.

        Added in GitLab all
        Available in GitLab Runner 0.4
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ci"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciApiV4Url")
    def ci_api_v4_url(cls) -> builtins.str:
        '''The GitLab API v4 root URL.

        Added in GitLab 11.7
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciApiV4Url"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciBuildsDir")
    def ci_builds_dir(cls) -> builtins.str:
        '''Top-level directory where builds are executed.

        Added in GitLab all
        Available in GitLab Runner 11.10
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciBuildsDir"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitBeforeSha")
    def ci_commit_before_sha(cls) -> builtins.str:
        '''The previous latest commit present on a branch. Is always 0000000000000000000000000000000000000000 in pipelines for merge requests.

        Added in GitLab 11.2
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitBeforeSha"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitDescription")
    def ci_commit_description(cls) -> builtins.str:
        '''The description of the commit the message without first line, if the title is shorter than 100 characters;

        full message in other case.

        Added in GitLab 10.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitDescription"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitMessage")
    def ci_commit_message(cls) -> builtins.str:
        '''The full commit message.

        Added in GitLab 10.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitMessage"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitRefName")
    def ci_commit_ref_name(cls) -> builtins.str:
        '''The branch or tag name for which project is built.

        Added in GitLab 9.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitRefName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitRefProtected")
    def ci_commit_ref_protected(cls) -> builtins.str:
        '''true if the job is running on a protected reference, false if not.

        Added in GitLab 11.11
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitRefProtected"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitRefSlug")
    def ci_commit_ref_slug(cls) -> builtins.str:
        '''$CI_COMMIT_REF_NAME in lowercase, shortened to 63 bytes, and with everything except 0-9 and a-z replaced with -.

        No leading / trailing -. Use in URLs, host names and domain names.

        Added in GitLab 9.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitRefSlug"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitSha")
    def ci_commit_sha(cls) -> builtins.str:
        '''The commit revision for which project is built.

        Added in GitLab 9.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitSha"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitShortSha")
    def ci_commit_short_sha(cls) -> builtins.str:
        '''The first eight characters of CI_COMMIT_SHA.

        Added in GitLab 11.7
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitShortSha"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitTimestamp")
    def ci_commit_timestamp(cls) -> builtins.str:
        '''The timestamp of the commit in the ISO 8601 format.

        Added in GitLab 13.4
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitTimestamp"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitTitle")
    def ci_commit_title(cls) -> builtins.str:
        '''The title of the commit - the full first line of the message.

        Added in GitLab 10.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciCommitTitle"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciConcurrentId")
    def ci_concurrent_id(cls) -> builtins.str:
        '''Unique ID of build execution in a single executor.

        Added in GitLab all
        Available in GitLab Runner 11.10
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciConcurrentId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciConcurrentProjectId")
    def ci_concurrent_project_id(cls) -> builtins.str:
        '''Unique ID of build execution in a single executor and project.

        Added in GitLab all
        Available in GitLab Runner 11.10
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciConcurrentProjectId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciConfigPath")
    def ci_config_path(cls) -> builtins.str:
        '''The path to CI configuration file. Defaults to .gitlab-ci.yml.

        Added in GitLab 9.4
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciConfigPath"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDebugTrace")
    def ci_debug_trace(cls) -> builtins.str:
        '''Whether debug logging (tracing) is enabled.

        Added in GitLab all
        Available in GitLab Runner 1.7
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciDebugTrace"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDefaultBranch")
    def ci_default_branch(cls) -> builtins.str:
        '''The name of the default branch for the project.

        Added in GitLab 12.4
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciDefaultBranch"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDependencyProxyGroupImagePrefix")
    def ci_dependency_proxy_group_image_prefix(cls) -> builtins.str:
        '''The image prefix for pulling images through the Dependency Proxy.

        Added in GitLab 13.7
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciDependencyProxyGroupImagePrefix"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDependencyProxyPassword")
    def ci_dependency_proxy_password(cls) -> builtins.str:
        '''The password to use to pull images through the Dependency Proxy.

        ATTENTION: Contrary to most other variables in this class, this variable is not resolved at rendering
        time. Instead the variable string is returned, which is then resolved during pipeline execution.
        This is because the value contains sensitive information.

        Added in GitLab 13.7
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciDependencyProxyPassword"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDependencyProxyServer")
    def ci_dependency_proxy_server(cls) -> builtins.str:
        '''The server for logging in to the Dependency Proxy. This is equivalent to $CI_SERVER_HOST:$CI_SERVER_PORT.

        Added in GitLab 13.7
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciDependencyProxyServer"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDependencyProxyUser")
    def ci_dependency_proxy_user(cls) -> builtins.str:
        '''The username to use to pull images through the Dependency Proxy.

        Added in GitLab 13.7
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciDependencyProxyUser"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDeployPassword")
    def ci_deploy_password(cls) -> builtins.str:
        '''Authentication password of the GitLab Deploy Token, only present if the Project has one related.

        ATTENTION: Contrary to most other variables in this class, this variable is not resolved at rendering
        time. Instead the variable string is returned, which is then resolved during pipeline execution.
        This is because the value contains sensitive information.

        Added in GitLab 10.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciDeployPassword"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDeployUser")
    def ci_deploy_user(cls) -> builtins.str:
        '''Authentication username of the GitLab Deploy Token, only present if the Project has one related.

        Added in GitLab 10.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciDeployUser"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciJobId")
    def ci_job_id(cls) -> builtins.str:
        '''The unique ID of the current job that GitLab CI/CD uses internally.

        Added in GitLab 9.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciJobId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciJobImage")
    def ci_job_image(cls) -> builtins.str:
        '''The name of the image running the CI job.

        Added in GitLab 12.9
        Available in GitLab Runner 12.9
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciJobImage"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciJobJwt")
    def ci_job_jwt(cls) -> builtins.str:
        '''RS256 JSON web token that can be used for authenticating with third party systems that support JWT authentication, for example HashiCorp’s Vault.

        ATTENTION: Contrary to most other variables in this class, this variable is not resolved at rendering
        time. Instead the variable string is returned, which is then resolved during pipeline execution.
        This is because the value contains sensitive information.

        Added in GitLab 12.10
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciJobJwt"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciJobManual")
    def ci_job_manual(cls) -> builtins.str:
        '''The flag to indicate that job was manually started.

        Added in GitLab 8.12
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciJobManual"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciJobName")
    def ci_job_name(cls) -> builtins.str:
        '''The name of the job as defined in .gitlab-ci.yml.

        Added in GitLab 9.0
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciJobName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciJobStage")
    def ci_job_stage(cls) -> builtins.str:
        '''The name of the stage as defined in .gitlab-ci.yml.

        Added in GitLab 9.0
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciJobStage"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciJobStatus")
    def ci_job_status(cls) -> builtins.str:
        '''The state of the job as each runner stage is executed.

        Use with after_script where CI_JOB_STATUS can be either success,
        failed or canceled.

        Added in GitLab all
        Available in GitLab Runner 13.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciJobStatus"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciJobToken")
    def ci_job_token(cls) -> builtins.str:
        '''Token used for authenticating with a few API endpoints and downloading dependent repositories.

        The token is valid as long as the job is running.

        ATTENTION: Contrary to most other variables in this class, this variable is not resolved at rendering
        time. Instead the variable string is returned, which is then resolved during pipeline execution.
        This is because the value contains sensitive information.

        Added in GitLab 9.0
        Available in GitLab Runner 1.2
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciJobToken"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciJobUrl")
    def ci_job_url(cls) -> builtins.str:
        '''Job details URL.

        Added in GitLab 11.1
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciJobUrl"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestTargetBranchName")
    def ci_merge_request_target_branch_name(cls) -> builtins.str:
        '''The target branch name of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules syntax
        is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciMergeRequestTargetBranchName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestTargetBranchSha")
    def ci_merge_request_target_branch_sha(cls) -> builtins.str:
        '''The HEAD SHA of the target branch of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules
        syntax is used, the merge request is created, and the pipeline is a merged
        result pipeline.

        Added in GitLab 11.9
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciMergeRequestTargetBranchSha"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciNodeTotal")
    def ci_node_total(cls) -> builtins.str:
        '''Total number of instances of this job running in parallel.

        If the job is not parallelized, this variable is set to 1.

        Added in GitLab 11.5
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciNodeTotal"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciPagesDomain")
    def ci_pages_domain(cls) -> builtins.str:
        '''The configured domain that hosts GitLab Pages.

        Added in GitLab 11.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciPagesDomain"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciPagesUrl")
    def ci_pages_url(cls) -> builtins.str:
        '''URL to GitLab Pages-built pages. Always belongs to a subdomain of CI_PAGES_DOMAIN.

        Added in GitLab 11.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciPagesUrl"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciPipelineId")
    def ci_pipeline_id(cls) -> builtins.str:
        '''The instance-level ID of the current pipeline. This is a unique ID across all projects on GitLab.

        Added in GitLab 8.10
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciPipelineId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciPipelineIid")
    def ci_pipeline_iid(cls) -> builtins.str:
        '''The project-level IID (internal ID) of the current pipeline. This ID is unique for the current project.

        Added in GitLab 11.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciPipelineIid"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciPipelineSource")
    def ci_pipeline_source(cls) -> builtins.str:
        '''Indicates how the pipeline was triggered.

        Possible options are push, web, schedule, api, external, chat, webide,
        merge_request_event, external_pull_request_event, parent_pipeline,
        trigger, or pipeline.
        For pipelines created before GitLab 9.5, this is displayed as unknown.

        Added in GitLab 10.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciPipelineSource"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciPipelineTriggered")
    def ci_pipeline_triggered(cls) -> builtins.str:
        '''The flag to indicate that job was triggered.

        Added in GitLab all
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciPipelineTriggered"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciPipelineUrl")
    def ci_pipeline_url(cls) -> builtins.str:
        '''Pipeline details URL.

        Added in GitLab 11.1
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciPipelineUrl"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectConfigPath")
    def ci_project_config_path(cls) -> builtins.str:
        '''The CI configuration path for the project.

        Added in GitLab 13.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectConfigPath"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectDir")
    def ci_project_dir(cls) -> builtins.str:
        '''The full path where the repository is cloned and where the job is run.

        If the GitLab Runner builds_dir parameter is set, this variable is set
        relative to the value of builds_dir. For more information, see Advanced
        configuration for GitLab Runner.

        Added in GitLab all
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectDir"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectId")
    def ci_project_id(cls) -> builtins.str:
        '''The unique ID of the current project that GitLab CI/CD uses internally.

        Added in GitLab all
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectName")
    def ci_project_name(cls) -> builtins.str:
        '''The name of the directory for the project that is being built.

        For example, if the project URL is gitlab.example.com/group-name/project-1,
        the CI_PROJECT_NAME would be project-1.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectNamespace")
    def ci_project_namespace(cls) -> builtins.str:
        '''The project stage (username or group name) that is being built.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectNamespace"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectPath")
    def ci_project_path(cls) -> builtins.str:
        '''The stage with project name.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectPath"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectPathSlug")
    def ci_project_path_slug(cls) -> builtins.str:
        '''$CI_PROJECT_PATH in lowercase and with everything except 0-9 and a-z replaced with -. Use in URLs and domain names.

        Added in GitLab 9.3
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectPathSlug"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectRepositoryLanguages")
    def ci_project_repository_languages(cls) -> builtins.str:
        '''Comma-separated, lowercase list of the languages used in the repository (for example ruby,javascript,html,css).

        Added in GitLab 12.3
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectRepositoryLanguages"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectRootNamespace")
    def ci_project_root_namespace(cls) -> builtins.str:
        '''The root project stage (username or group name) that is being built.

        For example, if CI_PROJECT_NAMESPACE is root-group/child-group/grandchild-group,
        CI_PROJECT_ROOT_NAMESPACE would be root-group.

        Added in GitLab 13.2
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectRootNamespace"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectTitle")
    def ci_project_title(cls) -> builtins.str:
        '''The human-readable project name as displayed in the GitLab web interface.

        Added in GitLab 12.4
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectTitle"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectUrl")
    def ci_project_url(cls) -> builtins.str:
        '''The HTTP(S) address to access project.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectUrl"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciProjectVisibility")
    def ci_project_visibility(cls) -> builtins.str:
        '''The project visibility (internal, private, public).

        Added in GitLab 10.3
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciProjectVisibility"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRegistryPassword")
    def ci_registry_password(cls) -> builtins.str:
        '''The password to use to push containers to the GitLab Container Registry, for the current project.

        ATTENTION: Contrary to most other variables in this class, this variable is not resolved at rendering
        time. Instead the variable string is returned, which is then resolved during pipeline execution.
        This is because the value contains sensitive information.

        Added in GitLab 9.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciRegistryPassword"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRepositoryUrl")
    def ci_repository_url(cls) -> builtins.str:
        '''The URL to clone the Git repository.

        ATTENTION: Contrary to most other variables in this class, this variable is not resolved at rendering
        time. Instead the variable string is returned, which is then resolved during pipeline execution.
        This is because the value contains sensitive information.

        Added in GitLab 9.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciRepositoryUrl"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRunnerDescription")
    def ci_runner_description(cls) -> builtins.str:
        '''The description of the runner as saved in GitLab.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciRunnerDescription"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRunnerExecutableArch")
    def ci_runner_executable_arch(cls) -> builtins.str:
        '''The OS/architecture of the GitLab Runner executable (note that this is not necessarily the same as the environment of the executor).

        Added in GitLab all
        Available in GitLab Runner 10.6
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciRunnerExecutableArch"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRunnerId")
    def ci_runner_id(cls) -> builtins.str:
        '''The unique ID of runner being used.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciRunnerId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRunnerRevision")
    def ci_runner_revision(cls) -> builtins.str:
        '''GitLab Runner revision that is executing the current job.

        Added in GitLab all
        Available in GitLab Runner 10.6
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciRunnerRevision"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRunnerShortToken")
    def ci_runner_short_token(cls) -> builtins.str:
        '''First eight characters of the runner’s token used to authenticate new job requests. Used as the runner’s unique ID.

        ATTENTION: Contrary to most other variables in this class, this variable is not resolved at rendering
        time. Instead the variable string is returned, which is then resolved during pipeline execution.
        This is because the value contains sensitive information.

        Added in GitLab all
        Available in GitLab Runner 12.3
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciRunnerShortToken"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRunnerTags")
    def ci_runner_tags(cls) -> builtins.str:
        '''The defined runner tags.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciRunnerTags"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRunnerVersion")
    def ci_runner_version(cls) -> builtins.str:
        '''GitLab Runner version that is executing the current job.

        Added in GitLab all
        Available in GitLab Runner 10.6
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciRunnerVersion"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServer")
    def ci_server(cls) -> builtins.str:
        '''Mark that job is executed in CI environment.

        Added in GitLab all
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServer"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerHost")
    def ci_server_host(cls) -> builtins.str:
        '''Host component of the GitLab instance URL, without protocol and port (like gitlab.example.com).

        Added in GitLab 12.1
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerHost"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerName")
    def ci_server_name(cls) -> builtins.str:
        '''The name of CI server that is used to coordinate jobs.

        Added in GitLab all
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerPort")
    def ci_server_port(cls) -> builtins.str:
        '''Port component of the GitLab instance URL, without host and protocol (like 3000).

        Added in GitLab 12.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerPort"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerProtocol")
    def ci_server_protocol(cls) -> builtins.str:
        '''Protocol component of the GitLab instance URL, without host and port (like https).

        Added in GitLab 12.8
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerProtocol"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerRevision")
    def ci_server_revision(cls) -> builtins.str:
        '''GitLab revision that is used to schedule jobs.

        Added in GitLab all
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerRevision"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerUrl")
    def ci_server_url(cls) -> builtins.str:
        '''The base URL of the GitLab instance, including protocol and port (like https://gitlab.example.com:8080).

        Added in GitLab 12.7
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerUrl"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerVersion")
    def ci_server_version(cls) -> builtins.str:
        '''GitLab version that is used to schedule jobs.

        Added in GitLab all
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerVersion"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerVersionMajor")
    def ci_server_version_major(cls) -> builtins.str:
        '''GitLab version major component.

        Added in GitLab 11.4
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerVersionMajor"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerVersionMinor")
    def ci_server_version_minor(cls) -> builtins.str:
        '''GitLab version minor component.

        Added in GitLab 11.4
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerVersionMinor"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciServerVersionPatch")
    def ci_server_version_patch(cls) -> builtins.str:
        '''GitLab version patch component.

        Added in GitLab 11.4
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ciServerVersionPatch"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="gitlabCi")
    def gitlab_ci(cls) -> builtins.str:
        '''Mark that job is executed in GitLab CI/CD environment.

        Added in GitLab all
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "gitlabCi"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="gitlabFeatures")
    def gitlab_features(cls) -> builtins.str:
        '''The comma separated list of licensed features available for your instance and plan.

        Added in GitLab 10.6
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "gitlabFeatures"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="gitlabUserEmail")
    def gitlab_user_email(cls) -> builtins.str:
        '''The email of the user who started the job.

        Added in GitLab 8.12
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "gitlabUserEmail"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="gitlabUserId")
    def gitlab_user_id(cls) -> builtins.str:
        '''The ID of the user who started the job.

        Added in GitLab 8.12
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "gitlabUserId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="gitlabUserLogin")
    def gitlab_user_login(cls) -> builtins.str:
        '''The login username of the user who started the job.

        Added in GitLab 10.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "gitlabUserLogin"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="gitlabUserName")
    def gitlab_user_name(cls) -> builtins.str:
        '''The real name of the user who started the job.

        Added in GitLab 10.0
        Available in GitLab Runner all
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "gitlabUserName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitBranch")
    def ci_commit_branch(cls) -> typing.Optional[builtins.str]:
        '''The commit branch name.

        Present in branch pipelines,
        including pipelines for the default branch.
        Not present in merge request pipelines or tag pipelines.

        Added in GitLab 12.6
        Available in GitLab Runner 0.5
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciCommitBranch"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciCommitTag")
    def ci_commit_tag(cls) -> typing.Optional[builtins.str]:
        '''The commit tag name. Present only when building tags.

        Added in GitLab 9.0
        Available in GitLab Runner 0.5
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciCommitTag"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDeployFreeze")
    def ci_deploy_freeze(cls) -> typing.Optional[builtins.str]:
        '''Included with the value true if the pipeline runs during a deploy freeze window.

        Added in GitLab 13.2
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciDeployFreeze"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciDisposableEnvironment")
    def ci_disposable_environment(cls) -> typing.Optional[builtins.str]:
        '''Marks that the job is executed in a disposable environment (something that is created only for this job and disposed of/destroyed after the execution - all executors except shell and ssh).

        If the environment is disposable, it is set to true,
        otherwise it is not defined at all.

        Added in GitLab all
        Available in GitLab Runner 10.1
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciDisposableEnvironment"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciEnvironmentName")
    def ci_environment_name(cls) -> typing.Optional[builtins.str]:
        '''The name of the environment for this job. Only present if environment:name is set.

        Added in GitLab 8.15
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciEnvironmentName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciEnvironmentSlug")
    def ci_environment_slug(cls) -> typing.Optional[builtins.str]:
        '''A simplified version of the environment name, suitable for inclusion in DNS, URLs, Kubernetes labels, and so on.

        Only present if environment:name is set.

        Added in GitLab 8.15
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciEnvironmentSlug"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciEnvironmentUrl")
    def ci_environment_url(cls) -> typing.Optional[builtins.str]:
        '''The URL of the environment for this job. Only present if environment:url is set.

        Added in GitLab 9.3
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciEnvironmentUrl"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciExternalPullRequestIid")
    def ci_external_pull_request_iid(cls) -> typing.Optional[builtins.str]:
        '''Pull Request ID from GitHub if the pipelines are for external pull requests.

        Available only if only [external_pull_requests] or
        rules syntax is used and the pull request is open.

        Added in GitLab 12.3
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciExternalPullRequestIid"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciExternalPullRequestSourceBranchName")
    def ci_external_pull_request_source_branch_name(
        cls,
    ) -> typing.Optional[builtins.str]:
        '''The source branch name of the pull request if the pipelines are for external pull requests.

        Available only if only [external_pull_requests]
        or rules syntax is used and the pull request is open.

        Added in GitLab 12.3
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciExternalPullRequestSourceBranchName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciExternalPullRequestSourceBranchSha")
    def ci_external_pull_request_source_branch_sha(
        cls,
    ) -> typing.Optional[builtins.str]:
        '''The HEAD SHA of the source branch of the pull request if the pipelines are for external pull requests.

        Available only if only
        [external_pull_requests] or rules syntax is used and the pull
        request is open.

        Added in GitLab 12.3
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciExternalPullRequestSourceBranchSha"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciExternalPullRequestSourceRepository")
    def ci_external_pull_request_source_repository(
        cls,
    ) -> typing.Optional[builtins.str]:
        '''The source repository name of the pull request if the pipelines are for external pull requests.

        Available only if only
        [external_pull_requests] or rules syntax is used and
        the pull request is open.

        Added in GitLab 13.3
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciExternalPullRequestSourceRepository"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciExternalPullRequestTargetBranchName")
    def ci_external_pull_request_target_branch_name(
        cls,
    ) -> typing.Optional[builtins.str]:
        '''The target branch name of the pull request if the pipelines are for external pull requests.

        Available only if only [external_pull_requests]
        or rules syntax is used and the pull request is open.
        *
        Added in GitLab 12.3
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciExternalPullRequestTargetBranchName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciExternalPullRequestTargetBranchSha")
    def ci_external_pull_request_target_branch_sha(
        cls,
    ) -> typing.Optional[builtins.str]:
        '''The HEAD SHA of the target branch of the pull request if the pipelines are for external pull requests.

        Available only if only
        [external_pull_requests] or rules syntax is used and the pull
        request is open.

        Added in GitLab 12.3
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciExternalPullRequestTargetBranchSha"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciExternalPullRequestTargetRepository")
    def ci_external_pull_request_target_repository(
        cls,
    ) -> typing.Optional[builtins.str]:
        '''The target repository name of the pull request if the pipelines are for external pull requests.

        Available only if only
        [external_pull_requests] or rules syntax is used and the pull
        request is open.

        Added in GitLab 13.3
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciExternalPullRequestTargetRepository"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciHasOpenRequirements")
    def ci_has_open_requirements(cls) -> typing.Optional[builtins.str]:
        '''Included with the value true only if the pipeline’s project has any open requirements.

        Not included if there are no open requirements for
        the pipeline’s project.

        Added in GitLab 13.1
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciHasOpenRequirements"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciKubernetesActive")
    def ci_kubernetes_active(cls) -> typing.Optional[builtins.str]:
        '''Included with the value true only if the pipeline has a Kubernetes cluster available for deployments.

        Not included if no cluster is available.
        Can be used as an alternative to only:kubernetes/except:kubernetes
        with rules:if.

        Added in GitLab 13.0
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciKubernetesActive"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestAssignees")
    def ci_merge_request_assignees(cls) -> typing.Optional[builtins.str]:
        '''Comma-separated list of username(s) of assignee(s) for the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules syntax is used and the
        merge request is created.

        Added in GitLab 11.9
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestAssignees"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestDiffBaseSha")
    def ci_merge_request_diff_base_sha(cls) -> typing.Optional[builtins.str]:
        '''The base SHA of the merge request diff, if the pipelines are for merge requests.

        Added in GitLab 13.7
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestDiffBaseSha"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestDiffId")
    def ci_merge_request_diff_id(cls) -> typing.Optional[builtins.str]:
        '''The version of the merge request diff, if the pipelines are for merge requests.

        Added in GitLab 13.7
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestDiffId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestEventType")
    def ci_merge_request_event_type(cls) -> typing.Optional[builtins.str]:
        '''The event type of the merge request, if the pipelines are for merge requests. Can be detached, merged_result or merge_train.

        Added in GitLab 12.3
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestEventType"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestId")
    def ci_merge_request_id(cls) -> typing.Optional[builtins.str]:
        '''The instance-level ID of the merge request.

        Only available if the
        pipelines are for merge requests and the merge request is created.
        This is a unique ID across all projects on GitLab.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestIid")
    def ci_merge_request_iid(cls) -> typing.Optional[builtins.str]:
        '''The project-level IID (internal ID) of the merge request.

        Only available If the pipelines are for merge requests and the merge
        request is created. This ID is unique for the current project.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestIid"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestLabels")
    def ci_merge_request_labels(cls) -> typing.Optional[builtins.str]:
        '''Comma-separated label names of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules
        syntax is used and the merge request is created.

        Added in GitLab 11.9
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestLabels"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestMilestone")
    def ci_merge_request_milestone(cls) -> typing.Optional[builtins.str]:
        '''The milestone title of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules syntax is
        used and the merge request is created.

        Added in GitLab 11.9
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestMilestone"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestProjectId")
    def ci_merge_request_project_id(cls) -> typing.Optional[builtins.str]:
        '''The ID of the project of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules syntax
        is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestProjectId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestProjectPath")
    def ci_merge_request_project_path(cls) -> typing.Optional[builtins.str]:
        '''The path of the project of the merge request if the pipelines are for merge requests (for example stage/awesome-project).

        Available only
        if only [merge_requests] or rules syntax is used and the merge request
        is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestProjectPath"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestProjectUrl")
    def ci_merge_request_project_url(cls) -> typing.Optional[builtins.str]:
        '''The URL of the project of the merge request if the pipelines are for merge requests (for example http://192.168.10.15:3000/stage/awesome-project). Available only if only [merge_requests] or rules syntax is used and the merge request is created.   * Added in GitLab 11.6 Available in GitLab Runner all.'''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestProjectUrl"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestRefPath")
    def ci_merge_request_ref_path(cls) -> typing.Optional[builtins.str]:
        '''The ref path of the merge request if the pipelines are for merge requests.

        (for example refs/merge-requests/1/head). Available only if only
        [merge_requests] or rules syntax is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestRefPath"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestSourceBranchName")
    def ci_merge_request_source_branch_name(cls) -> typing.Optional[builtins.str]:
        '''The source branch name of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules syntax
        is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestSourceBranchName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestSourceBranchSha")
    def ci_merge_request_source_branch_sha(cls) -> typing.Optional[builtins.str]:
        '''The HEAD SHA of the source branch of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules
        syntax is used, the merge request is created, and the pipeline is a
        merged result pipeline.

        Added in GitLab 11.9
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestSourceBranchSha"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestSourceProjectId")
    def ci_merge_request_source_project_id(cls) -> typing.Optional[builtins.str]:
        '''The ID of the source project of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules
        syntax is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestSourceProjectId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestSourceProjectPath")
    def ci_merge_request_source_project_path(cls) -> typing.Optional[builtins.str]:
        '''The path of the source project of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or
        rules syntax is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestSourceProjectPath"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestSourceProjectUrl")
    def ci_merge_request_source_project_url(cls) -> typing.Optional[builtins.str]:
        '''The URL of the source project of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules
        syntax is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestSourceProjectUrl"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciMergeRequestTitle")
    def ci_merge_request_title(cls) -> typing.Optional[builtins.str]:
        '''The title of the merge request if the pipelines are for merge requests.

        Available only if only [merge_requests] or rules syntax is used and the
        merge request is created.

        Added in GitLab 11.9
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciMergeRequestTitle"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciNodeIndex")
    def ci_node_index(cls) -> typing.Optional[builtins.str]:
        '''Index of the job in the job set. If the job is not parallelized, this variable is not set.

        Added in GitLab 11.5
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciNodeIndex"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciOpenMergeRequests")
    def ci_open_merge_requests(cls) -> typing.Optional[builtins.str]:
        '''Available in branch and merge request pipelines.

        Contains a
        comma-separated list of up to four merge requests that use the current
        branch and project as the merge request source.
        For example gitlab-org/gitlab!333,gitlab-org/gitlab-foss!11.

        Added in GitLab 13.8
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciOpenMergeRequests"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRegistry")
    def ci_registry(cls) -> typing.Optional[builtins.str]:
        '''GitLab Container Registry. This variable includes a :port value if one has been specified in the registry configuration.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciRegistry"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRegistryImage")
    def ci_registry_image(cls) -> typing.Optional[builtins.str]:
        '''the address of the registry tied to the specific project.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciRegistryImage"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciRegistryUser")
    def ci_registry_user(cls) -> typing.Optional[builtins.str]:
        '''The username to use to push containers to the GitLab Container Registry, for the current project.

        Added in GitLab 9.0
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciRegistryUser"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ciSharedEnvironment")
    def ci_shared_environment(cls) -> typing.Optional[builtins.str]:
        '''Marks that the job is executed in a shared environment (something that is persisted across CI invocations like shell or ssh executor).

        If the environment is shared, it is set to true, otherwise it is not
        defined at all.

        Added in GitLab all
        Available in GitLab Runner 10.1
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "ciSharedEnvironment"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="triggerPayload")
    def trigger_payload(cls) -> typing.Optional[builtins.str]:
        '''This variable is available when a pipeline is triggered with a webhook.

        Added in GitLab 13.9
        Available in GitLab Runner all
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.sget(cls, "triggerPayload"))


@jsii.data_type(
    jsii_type="@gcix/gcix.RenderedImage",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "entrypoint": "entrypoint"},
)
class RenderedImage:
    def __init__(
        self,
        *,
        name: builtins.str,
        entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''This module represents the Gitlab CI `Image <https://docs.gitlab.com/ee/ci/yaml/#image>`_ keyword. Use ``Image`` to specify a Docker image to use for the ``gcix.Job``.

        Instances of this class are intended to be immutable. Image objects are
        typically defined in a central location and often reused throughout the
        codebase. Modifying an Image object at one place may result in unexpected
        changes at any other reference to that object. Therefore, this class does
        not provide any setter methods to modify its properties directly.

        However, you can create an altered copy of an Image object using
        the .withTag() and .withEntrypoint() methods. These methods return a new
        Image object with the specified modifications, allowing you to reuse the
        original Image object while making specific changes for a particular use case.

        By following this approach, you can maintain a central repository of Image
        objects and easily create customized versions as needed, without affecting
        the original object or introducing unintended side effects.

        :param name: 
        :param entrypoint: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62130a6aedd9621ef44fbfbd39f522f363028ee02b9197019c7ef95347186b45)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument entrypoint", value=entrypoint, expected_type=type_hints["entrypoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderedImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.RenderedIncludeArtifact",
    jsii_struct_bases=[],
    name_mapping={"artifact": "artifact", "job": "job"},
)
class RenderedIncludeArtifact:
    def __init__(self, *, artifact: builtins.str, job: builtins.str) -> None:
        '''
        :param artifact: 
        :param job: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaec6b0c2f5b9bc0a3b9ba0d4306036a9874070bd74d94baf8eb41cb0e0d01ba)
            check_type(argname="argument artifact", value=artifact, expected_type=type_hints["artifact"])
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact": artifact,
            "job": job,
        }

    @builtins.property
    def artifact(self) -> builtins.str:
        result = self._values.get("artifact")
        assert result is not None, "Required property 'artifact' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job(self) -> builtins.str:
        result = self._values.get("job")
        assert result is not None, "Required property 'job' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderedIncludeArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.RenderedIncludeFile",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "project": "project", "ref": "ref"},
)
class RenderedIncludeFile:
    def __init__(
        self,
        *,
        file: builtins.str,
        project: builtins.str,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: 
        :param project: 
        :param ref: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e290ea0424ed1cf5a990f17ec7c453ad9292c275effb7a29d65ce8d13546fed5)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file": file,
            "project": project,
        }
        if ref is not None:
            self._values["ref"] = ref

    @builtins.property
    def file(self) -> builtins.str:
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project(self) -> builtins.str:
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderedIncludeFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.RenderedIncludeLocal",
    jsii_struct_bases=[],
    name_mapping={"local": "local"},
)
class RenderedIncludeLocal:
    def __init__(self, *, local: builtins.str) -> None:
        '''
        :param local: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb630516648dea763828c2937fd40f93a61f3780f9034b0f797637733fcce359)
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local": local,
        }

    @builtins.property
    def local(self) -> builtins.str:
        result = self._values.get("local")
        assert result is not None, "Required property 'local' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderedIncludeLocal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.RenderedIncludeRemote",
    jsii_struct_bases=[],
    name_mapping={"remote": "remote"},
)
class RenderedIncludeRemote:
    def __init__(self, *, remote: builtins.str) -> None:
        '''
        :param remote: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767f6aeebc514bdd0379b807bd7e8f1439350f3f143031e04168d9b6054cc8b6)
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote": remote,
        }

    @builtins.property
    def remote(self) -> builtins.str:
        result = self._values.get("remote")
        assert result is not None, "Required property 'remote' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderedIncludeRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.RenderedIncludeTemplate",
    jsii_struct_bases=[],
    name_mapping={"template": "template"},
)
class RenderedIncludeTemplate:
    def __init__(self, *, template: builtins.str) -> None:
        '''
        :param template: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643d1588e9d2e97427d55878c322abc5efae9e1fe124db975f524a7d9aca0613)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template": template,
        }

    @builtins.property
    def template(self) -> builtins.str:
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderedIncludeTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.RenderedJob",
    jsii_struct_bases=[],
    name_mapping={},
)
class RenderedJob:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderedJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRule)
class Rule(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.Rule"):
    def __init__(
        self,
        *,
        allow_failure: typing.Optional[builtins.bool] = None,
        changes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exists: typing.Optional[typing.Sequence[builtins.str]] = None,
        if_statement: typing.Optional[builtins.str] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        when: typing.Optional["WhenStatement"] = None,
    ) -> None:
        '''
        :param allow_failure: Default: false
        :param changes: 
        :param exists: 
        :param if_statement: 
        :param variables: 
        :param when: Default: WhenStatement.ON_SUCCESS.
        '''
        props = RuleProps(
            allow_failure=allow_failure,
            changes=changes,
            exists=exists,
            if_statement=if_statement,
            variables=variables,
            when=when,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addVariables")
    def add_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "Rule":
        '''Adds one or more `variables <https://docs.gitlab.com/ee/ci/yaml/README.html#variables>`_, each as keyword argument, to the rule.

        Example::

           rule.addVariables({GREETING: "hello", LANGUAGE: "typescript"})

        :param variables: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dada20c2e64f84ae5060483b9b519132f4a6f47602899f297ee58bbfe0851d0)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("Rule", jsii.invoke(self, "addVariables", [variables]))

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7b865315adc72624c1abac74f9baa2656c915682f30f394e525f01389e9e5b)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="never")
    def never(self) -> "Rule":
        '''This method is intended to be used for predefined rules.

        For instance you have defined an
        often used rule ``on_master`` whose if statement checks if the pipeline is executed on branch
        ``master``. Then you can either run a job, if on master..::

           myJob.appendRules(onMaster)

        ... or do not run a job if on master..::

           myJob.appendRules(onMaster.never())
        '''
        return typing.cast("Rule", jsii.invoke(self, "never", []))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.

        :return: RenderedRule
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "variables"))

    @variables.setter
    def variables(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e95b6f4a18d08cc8e3002a85450b2840df6eb98bd3fa63a82a70bef3b8f0cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variables", value)

    @builtins.property
    @jsii.member(jsii_name="allowFailure")
    def allow_failure(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "allowFailure"))

    @allow_failure.setter
    def allow_failure(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe70022e9cc65c6beebd39215d6178cb4cceef6e8d05f8031aed0b2807215d9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailure", value)

    @builtins.property
    @jsii.member(jsii_name="changes")
    def changes(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "changes"))

    @changes.setter
    def changes(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e69f846467e29c36ad300c3fe972f7bbb8526d62c4dc20207b7649e68b37239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changes", value)

    @builtins.property
    @jsii.member(jsii_name="exists")
    def exists(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exists"))

    @exists.setter
    def exists(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7010546164a533f917900ba07195dd9d0e42527a106aad1ea5041884ec33bf48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exists", value)

    @builtins.property
    @jsii.member(jsii_name="ifStatement")
    def if_statement(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ifStatement"))

    @if_statement.setter
    def if_statement(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0dbb3e348c8c2582f4c3d2c0c0917223d347c97f3b53680906c3148b8ddec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ifStatement", value)

    @builtins.property
    @jsii.member(jsii_name="when")
    def when(self) -> typing.Optional["WhenStatement"]:
        return typing.cast(typing.Optional["WhenStatement"], jsii.get(self, "when"))

    @when.setter
    def when(self, value: typing.Optional["WhenStatement"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081adca324252fb94113a3c885f81b46fd8c1512eaa37200e22e7e17a416baaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "when", value)


class RuleLib(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.RuleLib"):
    '''Represents a library of static methods to create rules for GitLab CI/CD pipeline conditions.'''

    @jsii.member(jsii_name="notOnBranch")
    @builtins.classmethod
    def not_on_branch(cls, branch_name: builtins.str) -> Rule:
        '''Creates a rule that evaluates to true if the CI/CD pipeline is NOT running on the specified branch.

        :param branch_name: - The name of the branch to check.

        :return: A ``Rule`` object representing the condition for NOT being on the specified branch.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883b6a68a81893d6c9ded08f6240471fb8ebaf9608da477eda62eced7c143d0b)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
        return typing.cast(Rule, jsii.sinvoke(cls, "notOnBranch", [branch_name]))

    @jsii.member(jsii_name="notOnMain")
    @builtins.classmethod
    def not_on_main(cls) -> Rule:
        '''Creates a rule that evaluates to true if the CI/CD pipeline is NOT running on the "main" branch.

        :return: A ``Rule`` object representing the condition for NOT being on the "main" branch.
        '''
        return typing.cast(Rule, jsii.sinvoke(cls, "notOnMain", []))

    @jsii.member(jsii_name="notOnMaster")
    @builtins.classmethod
    def not_on_master(cls) -> Rule:
        '''Creates a rule that evaluates to true if the CI/CD pipeline is NOT running on the "master" branch.

        :return: A ``Rule`` object representing the condition for NOT being on the "master" branch.
        '''
        return typing.cast(Rule, jsii.sinvoke(cls, "notOnMaster", []))

    @jsii.member(jsii_name="onBranch")
    @builtins.classmethod
    def on_branch(cls, branch_name: builtins.str) -> Rule:
        '''Creates a rule that evaluates to true if the CI/CD pipeline is running on the specified branch.

        :param branch_name: - The name of the branch to check.

        :return: A ``Rule`` object representing the condition for the specified branch.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d49c4831cdafc79824344b9e38c01b0a4c349904e595164e602e76d9038236a)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
        return typing.cast(Rule, jsii.sinvoke(cls, "onBranch", [branch_name]))

    @jsii.member(jsii_name="onMain")
    @builtins.classmethod
    def on_main(cls) -> Rule:
        '''Creates a rule that evaluates to true if the CI/CD pipeline is running on the "main" branch.

        :return: A ``Rule`` object representing the condition for the "main" branch.
        '''
        return typing.cast(Rule, jsii.sinvoke(cls, "onMain", []))

    @jsii.member(jsii_name="onMaster")
    @builtins.classmethod
    def on_master(cls) -> Rule:
        '''Creates a rule that evaluates to true if the CI/CD pipeline is running on the "master" branch.

        :return: A ``Rule`` object representing the condition for the "master" branch.
        '''
        return typing.cast(Rule, jsii.sinvoke(cls, "onMaster", []))

    @jsii.member(jsii_name="onMergeRequestEvents")
    @builtins.classmethod
    def on_merge_request_events(cls) -> Rule:
        '''Creates a rule that evaluates to true for merge request events in the CI/CD pipeline.

        :return: A ``Rule`` object representing the condition for merge request events.
        '''
        return typing.cast(Rule, jsii.sinvoke(cls, "onMergeRequestEvents", []))

    @jsii.member(jsii_name="onPipelineTrigger")
    @builtins.classmethod
    def on_pipeline_trigger(cls) -> Rule:
        '''Creates a rule that evaluates to true for pipelines triggered by API or the trigger keyword.

        :return: A ``Rule`` object representing the condition for pipeline triggers.
        '''
        return typing.cast(Rule, jsii.sinvoke(cls, "onPipelineTrigger", []))

    @jsii.member(jsii_name="onSuccess")
    @builtins.classmethod
    def on_success(cls) -> Rule:
        '''Creates a rule that always evaluates to true (success).

        :return: A ``Rule`` object representing a success condition.
        '''
        return typing.cast(Rule, jsii.sinvoke(cls, "onSuccess", []))

    @jsii.member(jsii_name="onTags")
    @builtins.classmethod
    def on_tags(cls) -> Rule:
        '''Creates a rule that evaluates to true for CI/CD pipelines triggered by tags.

        :return: A ``Rule`` object representing the condition for tag-based pipelines.
        '''
        return typing.cast(Rule, jsii.sinvoke(cls, "onTags", []))


@jsii.data_type(
    jsii_type="@gcix/gcix.RuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_failure": "allowFailure",
        "changes": "changes",
        "exists": "exists",
        "if_statement": "ifStatement",
        "variables": "variables",
        "when": "when",
    },
)
class RuleProps:
    def __init__(
        self,
        *,
        allow_failure: typing.Optional[builtins.bool] = None,
        changes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exists: typing.Optional[typing.Sequence[builtins.str]] = None,
        if_statement: typing.Optional[builtins.str] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        when: typing.Optional["WhenStatement"] = None,
    ) -> None:
        '''
        :param allow_failure: Default: false
        :param changes: 
        :param exists: 
        :param if_statement: 
        :param variables: 
        :param when: Default: WhenStatement.ON_SUCCESS.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17680b9412fcc8a61ed4dd9ab67d6f960ee608993fab721fe7cd21eae45fbe1d)
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
            check_type(argname="argument changes", value=changes, expected_type=type_hints["changes"])
            check_type(argname="argument exists", value=exists, expected_type=type_hints["exists"])
            check_type(argname="argument if_statement", value=if_statement, expected_type=type_hints["if_statement"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_failure is not None:
            self._values["allow_failure"] = allow_failure
        if changes is not None:
            self._values["changes"] = changes
        if exists is not None:
            self._values["exists"] = exists
        if if_statement is not None:
            self._values["if_statement"] = if_statement
        if variables is not None:
            self._values["variables"] = variables
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def allow_failure(self) -> typing.Optional[builtins.bool]:
        '''
        :default: false

        :description:

        The `allow_failure <https://docs.gitlab.com/ee/ci/yaml/#allow_failure>`_
        attribute which let a job fail without impacting the rest of the CI suite.
        '''
        result = self._values.get("allow_failure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def changes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :description:

        The `changes <https://docs.gitlab.com/ee/ci/yaml/#ruleschanges>`_
        attribute which adds a job to the pipeline by checking for changes on specific files
        '''
        result = self._values.get("changes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exists(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :description:

        The `exists <https://docs.gitlab.com/ee/ci/yaml/#rulesexists>`_
        attribute which allows to run a job when a certain files exist in the repository
        '''
        result = self._values.get("exists")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def if_statement(self) -> typing.Optional[builtins.str]:
        '''
        :description:

        The `rules:if clause <https://docs.gitlab.com/ee/ci/yaml/#when>`_
        which decides when a job to the pipeline.
        '''
        result = self._values.get("if_statement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :description:

        The `variables <https://docs.gitlab.com/ee/ci/yaml/#rulesvariables>`_
        attribute allows defining or overwriting variables when the conditions are met
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def when(self) -> typing.Optional["WhenStatement"]:
        '''
        :default: WhenStatement.ON_SUCCESS.

        :description:

        The `when <https://docs.gitlab.com/ee/ci/yaml/#when>`_
        attribute which decides when to run a job.
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional["WhenStatement"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IService)
class Service(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.Service"):
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: 
        '''
        props = ServiceProps(name=name)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36137733761a8c4aed62db7162c6232d0355ca060632e46c88c978da9197a6d6)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@gcix/gcix.ServiceProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ServiceProps:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: 

        :todo:

        **ALPHA** This module represents the Gitlab CI
        `Service <https://docs.gitlab.com/ee/ci/yaml/README.html#services>`_ keyword.

        The services keyword defines a Docker image that runs during a job linked
        to the Docker image that the image keyword defines.
        This allows you to access the service image during build time.

        Currently this module is an unfinished prototype.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebdd539c170dac097bec6b0c36f2d9cbb28b7272f0addd02ee7f5a57e13c8bf7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gcix/gcix.TriggerJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "includes": "includes",
        "name": "name",
        "project": "project",
        "stage": "stage",
        "strategy": "strategy",
    },
)
class TriggerJobProps:
    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        includes: typing.Optional[typing.Sequence[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: 
        :param includes: 
        :param name: 
        :param project: 
        :param stage: 
        :param strategy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a9bec0136da3d138ee5524a6e20dc4924dce668845b921e31d0fbc1f1a6d31)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch is not None:
            self._values["branch"] = branch
        if includes is not None:
            self._values["includes"] = includes
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if stage is not None:
            self._values["stage"] = stage
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''
        :description: The branch of ``project`` the pipeline should be triggered of.
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def includes(
        self,
    ) -> typing.Optional[typing.List[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]]:
        '''
        :description:

        Include a pipeline to trigger (Parent-child pipeline trigger)
        Mutually exclusiv with ``project``.
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :description: The name of the trigger job.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''
        :description:

        The full name of another Gitlab project to trigger
        (multi-project pipeline trigger). Mutually exclusive with ``includes``.
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''
        :description: The stage of the trigger job.
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strategy(self) -> typing.Optional[builtins.str]:
        '''
        :description:

        Determines if the result of this pipeline depends on the
        triggered downstream pipeline (use ``TriggerStrategy.DEPEND``) or if just
        "fire and forget" the downstream pipeline.

        Use ``depend`` to force the ``TriggerJob`` to wait for the downstream
        (multi-project or child) pipeline to complete.
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TriggerJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@gcix/gcix.WhenStatement")
class WhenStatement(enum.Enum):
    '''This enum holds different `when <https://docs.gitlab.com/ee/ci/yaml/#when>`_ statements for ``Rule``s.'''

    ALWAYS = "ALWAYS"
    DELAYED = "DELAYED"
    MANUAL = "MANUAL"
    NEVER = "NEVER"
    ONFAILURE = "ONFAILURE"
    ONSUCCESS = "ONSUCCESS"


@jsii.implements(ICache)
class Cache(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.Cache"):
    '''This class represents the `cache <https://docs.gitlab.com/ee/ci/yaml/#cache>`_ keyword.

    Gitlab CI documentation:

    *"Use cache to specify a list of files and directories to cache between
    ``gcix.Job``s. [...] Caching is shared between
    ``gcix.Pipeline``s and ``gcix.Job``s.
    Caches are restored before artifacts."*

    :throws: ``Error`` for unsupported ``when`` values.
    '''

    def __init__(
        self,
        *,
        paths: typing.Sequence[builtins.str],
        cache_key: typing.Optional["CacheKey"] = None,
        policy: typing.Optional[CachePolicy] = None,
        untracked: typing.Optional[builtins.bool] = None,
        when: typing.Optional[WhenStatement] = None,
    ) -> None:
        '''
        :param paths: 
        :param cache_key: Default: to ``CacheKey`` with default arguments.
        :param policy: 
        :param untracked: Set the `untracked keyword <https://docs.gitlab.com/ee/ci/yaml/#cacheuntracked>`_ to ``True`` to cache all files that are untracked in your Git repository.
        :param when: 
        '''
        props = CacheProps(
            paths=paths,
            cache_key=cache_key,
            policy=policy,
            untracked=untracked,
            when=when,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0183fdae5917a8cf383d235801473da1787225eaa02ab9ccff24a1bef7cc8738)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.

        :return: RenderedCache
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="cacheKey")
    def cache_key(self) -> "CacheKey":
        return typing.cast("CacheKey", jsii.get(self, "cacheKey"))

    @cache_key.setter
    def cache_key(self, value: "CacheKey") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86e4fdcf9090775a868778e504b137a9c582c41ee934974f4f778cae6c6d5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheKey", value)

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ae9ebf898d16c4f90435ef91068c2c0129887233421de38891ea963a586517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[CachePolicy]:
        return typing.cast(typing.Optional[CachePolicy], jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Optional[CachePolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b191468d86faae5a5ae68371c5ececb432d5a7b3e2432f08597a988c82123113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="untracked")
    def untracked(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "untracked"))

    @untracked.setter
    def untracked(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9981b23dea0fefe2c794065c6a2610d50177a89dc0d081cfb5510c0e0ba4b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "untracked", value)

    @builtins.property
    @jsii.member(jsii_name="when")
    def when(self) -> typing.Optional[WhenStatement]:
        return typing.cast(typing.Optional[WhenStatement], jsii.get(self, "when"))

    @when.setter
    def when(self, value: typing.Optional[WhenStatement]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5413ae83fada192ab46461a6b711b3e34dd05fcf981f785326131006a4d7ba73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "when", value)


@jsii.implements(ICacheKey)
class CacheKey(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.CacheKey"):
    '''This class represents the `cache:key <https://docs.gitlab.com/ee/ci/yaml/#cachekey>`_ keyword.

    Gitlab CI documentation: *"The key keyword defines the affinity of caching
    between jobs. You can have a single cache for all jobs, cache per-job,
    cache per-branch, or any other way that fits your workflow."*

    :throws: Error if ``prefix`` but not ``files`` is provided.
    '''

    def __init__(
        self,
        *,
        files: typing.Optional[typing.Sequence[builtins.str]] = None,
        key: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param files: 
        :param key: Default: gcix.PredefinedVariables.ciCommitRefSlug
        :param prefix: 
        '''
        props = CacheKeyProps(files=files, key=key, prefix=prefix)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31e0b17fe36d665eeeef4e7aedceef00c8cb9509deaa146ca235892d42339ed)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.

        :return: RenderedCacheKey
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="files")
    def files(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "files"))

    @files.setter
    def files(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a0620d883946f34a3867e71556506f18a2b690d9be847becc7d127f1bb243c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "files", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "key"))

    @key.setter
    def key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b14df8ab7205cb996776eacabc1a3c8e2a1f108f573daf0164a92c74bb262b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94e85a980c5516fee35ca39218361f799e4876b39b2c3ac9c8ce8dba86c1951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.interface(jsii_type="@gcix/gcix.IArtifacts")
class IArtifacts(IBase, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="expireIn")
    def expire_in(self) -> typing.Optional[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="exposeAs")
    def expose_as(self) -> typing.Optional[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="public")
    def public(self) -> typing.Optional[builtins.bool]:
        ...

    @builtins.property
    @jsii.member(jsii_name="reports")
    def reports(self) -> typing.Optional[typing.List[ArtifactsReport]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="untracked")
    def untracked(self) -> typing.Optional[builtins.bool]:
        ...

    @builtins.property
    @jsii.member(jsii_name="when")
    def when(self) -> typing.Optional[WhenStatement]:
        ...

    @jsii.member(jsii_name="addExcludes")
    def add_excludes(self, excludes: typing.Sequence[builtins.str]) -> None:
        '''
        :param excludes: -
        '''
        ...

    @jsii.member(jsii_name="addPaths")
    def add_paths(self, paths: typing.Sequence[builtins.str]) -> None:
        '''
        :param paths: -
        '''
        ...


class _IArtifactsProxy(
    jsii.proxy_for(IBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IArtifacts"

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @builtins.property
    @jsii.member(jsii_name="expireIn")
    def expire_in(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expireIn"))

    @builtins.property
    @jsii.member(jsii_name="exposeAs")
    def expose_as(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exposeAs"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="public")
    def public(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "public"))

    @builtins.property
    @jsii.member(jsii_name="reports")
    def reports(self) -> typing.Optional[typing.List[ArtifactsReport]]:
        return typing.cast(typing.Optional[typing.List[ArtifactsReport]], jsii.get(self, "reports"))

    @builtins.property
    @jsii.member(jsii_name="untracked")
    def untracked(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "untracked"))

    @builtins.property
    @jsii.member(jsii_name="when")
    def when(self) -> typing.Optional[WhenStatement]:
        return typing.cast(typing.Optional[WhenStatement], jsii.get(self, "when"))

    @jsii.member(jsii_name="addExcludes")
    def add_excludes(self, excludes: typing.Sequence[builtins.str]) -> None:
        '''
        :param excludes: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b5b8c4ba7633202752f68da52f6ea66904445bf79b755180cf48d82eff0b7f2)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
        return typing.cast(None, jsii.invoke(self, "addExcludes", [excludes]))

    @jsii.member(jsii_name="addPaths")
    def add_paths(self, paths: typing.Sequence[builtins.str]) -> None:
        '''
        :param paths: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7614a51c2e49545a8ed8d70ff4ed30c7fe5673edaaf959336145530398444f2)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        return typing.cast(None, jsii.invoke(self, "addPaths", [paths]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IArtifacts).__jsii_proxy_class__ = lambda : _IArtifactsProxy


@jsii.interface(jsii_type="@gcix/gcix.IJob")
class IJob(IJobBase, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="original")
    def original(self) -> typing.Optional["Job"]:
        ...

    @original.setter
    def original(self, value: typing.Optional["Job"]) -> None:
        ...

    @jsii.member(jsii_name="addParent")
    def add_parent(self, parent: typing.Union["Job", "JobCollection"]) -> None:
        '''This method is called by ``gcix.JobCollection``s when the job is added to that JobCollection.

        The job needs to know its parents when ``getAllInstanceNames()`` is called.

        :param parent: any type of Job or JobCollection.
        '''
        ...

    @jsii.member(jsii_name="assignAllowFailure")
    def assign_allow_failure(
        self,
        allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
    ) -> "Job":
        '''
        :param allow_failure: -

        :description: Sets ``allowFailure`` for this job.
        '''
        ...

    @jsii.member(jsii_name="assignDependencies")
    def assign_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "Job":
        '''
        :param dependencies: -

        :description:

        Set the list of `dependencies <https://docs.gitlab.com/ee/ci/yaml/index.html#dependencies>`_ of this job.

        !! Any previous values will be overwritten.
        '''
        ...

    @jsii.member(jsii_name="assignImage")
    def assign_image(self, image: typing.Union[builtins.str, Image]) -> "Job":
        '''Sets the image of this job.

        For a simple container image you can provide the origin of the image.
        If you want to set the entrypoint, you have to provide an Image object instead.

        !! Any previous values will be overwritten.

        :param image: -

        :return: Job the modified ``Job`` object.
        '''
        ...

    @jsii.member(jsii_name="assignNeeds")
    def assign_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "Job":
        '''
        :param needs: -

        :description: Set the list of `needs <https://docs.gitlab.com/ee/ci/yaml/README.html#needs>`_ of this job.
        '''
        ...

    @jsii.member(jsii_name="assignTags")
    def assign_tags(self, tags: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param tags: -

        :description:

        Set the `tags <https://docs.gitlab.com/ee/ci/yaml/README.html#tags>`_ to the job.

        !! Any previous values will be overwritten.
        '''
        ...

    @jsii.member(jsii_name="copy")
    def copy(self) -> "Job":
        '''Returns an independent, deep copy object of this job.'''
        ...

    @jsii.member(jsii_name="extendName")
    def extend_name(self, name: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs name.

        :param name: to append to the current name.
        '''
        ...

    @jsii.member(jsii_name="extendStage")
    def extend_stage(self, stage: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs name and stage.

        :param stage: name to extend the stage and the name.
        '''
        ...

    @jsii.member(jsii_name="extendStageValue")
    def extend_stage_value(self, stage: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs stage.

        :param stage: name to extend the stage.
        '''
        ...


class _IJobProxy(
    jsii.proxy_for(IJobBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IJob"

    @builtins.property
    @jsii.member(jsii_name="original")
    def original(self) -> typing.Optional["Job"]:
        return typing.cast(typing.Optional["Job"], jsii.get(self, "original"))

    @original.setter
    def original(self, value: typing.Optional["Job"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf96137fbb57c57d1030d349ff02fbd74594d2f66b12e7d4c0bb4f274d4cfc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "original", value)

    @jsii.member(jsii_name="addParent")
    def add_parent(self, parent: typing.Union["Job", "JobCollection"]) -> None:
        '''This method is called by ``gcix.JobCollection``s when the job is added to that JobCollection.

        The job needs to know its parents when ``getAllInstanceNames()`` is called.

        :param parent: any type of Job or JobCollection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a134b11e1ad65606a69cc0c5e4d9d932441690495879985927dbb1db87638088)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
        return typing.cast(None, jsii.invoke(self, "addParent", [parent]))

    @jsii.member(jsii_name="assignAllowFailure")
    def assign_allow_failure(
        self,
        allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
    ) -> "Job":
        '''
        :param allow_failure: -

        :description: Sets ``allowFailure`` for this job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a9854a6cdb23124efa141c8b9b00ba0ef2bf8250867ae138d16604d0b51e4f)
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
        return typing.cast("Job", jsii.invoke(self, "assignAllowFailure", [allow_failure]))

    @jsii.member(jsii_name="assignDependencies")
    def assign_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "Job":
        '''
        :param dependencies: -

        :description:

        Set the list of `dependencies <https://docs.gitlab.com/ee/ci/yaml/index.html#dependencies>`_ of this job.

        !! Any previous values will be overwritten.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7730f2ccc4b8c9213f50f0e50d1c46902750aa724adf2c4e23378dd11e5be925)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("Job", jsii.invoke(self, "assignDependencies", [dependencies]))

    @jsii.member(jsii_name="assignImage")
    def assign_image(self, image: typing.Union[builtins.str, Image]) -> "Job":
        '''Sets the image of this job.

        For a simple container image you can provide the origin of the image.
        If you want to set the entrypoint, you have to provide an Image object instead.

        !! Any previous values will be overwritten.

        :param image: -

        :return: Job the modified ``Job`` object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbcdcaec0006e696ba00afc16746dda9ba125b27ceb67584a6c7196c6f9e9cc)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast("Job", jsii.invoke(self, "assignImage", [image]))

    @jsii.member(jsii_name="assignNeeds")
    def assign_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "Job":
        '''
        :param needs: -

        :description: Set the list of `needs <https://docs.gitlab.com/ee/ci/yaml/README.html#needs>`_ of this job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46bcc7245d8c2b9e48b79b3c95ef4f945046523a8c28f0da061549043a6fdab7)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("Job", jsii.invoke(self, "assignNeeds", [needs]))

    @jsii.member(jsii_name="assignTags")
    def assign_tags(self, tags: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param tags: -

        :description:

        Set the `tags <https://docs.gitlab.com/ee/ci/yaml/README.html#tags>`_ to the job.

        !! Any previous values will be overwritten.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad29f55eaaabf289c63253da4efa91842cb25be90c6877f1ddc74036ce79ac1)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("Job", jsii.invoke(self, "assignTags", [tags]))

    @jsii.member(jsii_name="copy")
    def copy(self) -> "Job":
        '''Returns an independent, deep copy object of this job.'''
        return typing.cast("Job", jsii.invoke(self, "copy", []))

    @jsii.member(jsii_name="extendName")
    def extend_name(self, name: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs name.

        :param name: to append to the current name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f664bbcc750184adaa32f039a01fe87ccabef41cf30faa1e91995d0beaa112a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "extendName", [name]))

    @jsii.member(jsii_name="extendStage")
    def extend_stage(self, stage: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs name and stage.

        :param stage: name to extend the stage and the name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2f2b757cb76f3fa887f7a5caffd94fe9a339333d431666c4c7905f3488177d)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast(None, jsii.invoke(self, "extendStage", [stage]))

    @jsii.member(jsii_name="extendStageValue")
    def extend_stage_value(self, stage: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs stage.

        :param stage: name to extend the stage.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37512d3f1c106d4b00d4ea2427bdc75dac56aa97bad4983020ac437339ee9b4)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast(None, jsii.invoke(self, "extendStageValue", [stage]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJob).__jsii_proxy_class__ = lambda : _IJobProxy


@jsii.interface(jsii_type="@gcix/gcix.IJobCollection")
class IJobCollection(IJobCollectionBase, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="lastJobsExecuted")
    def last_jobs_executed(self) -> typing.List["Job"]:
        '''This property returns all Jobs from the last stage of this JobCollection.

        This is typically be requested from a job which has setup this
        JobCollection as need, to determine all actual jobs of this JobCollection
        as need.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="nestedJobs")
    def nested_jobs(self) -> typing.List["Job"]:
        '''
        :return:

        all jobs of this this JobCollection as well as jobs of
        sub-JobCollection recursively.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="populatedJobs")
    def populated_jobs(self) -> typing.List["Job"]:
        '''Returns a list with populated copies of all nested jobs of this JobCollection.

        Populated means, that all attributes of a Job which depends on its context
        are resolved to their final values. The context is primarily the
        JobCollection within the jobs resides but also dependencies to other
        jobs and JobCollection's. Thus this JobCollection will apply its own
        configuration, like variables to add, tags to set, etc., to all its jobs
        and JobCollection's.

        Copies means what it says, that the returned job are not the same job
        objects, originally added to this JobCollection, but copies of them.

        Nested means, that also jobs from JobCollection's within this
        JobCollection, are returned, as well as jobs from JobCollection's within
        JobCollection's within this JobCollection and so on.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List[ChildDict]:
        ...

    @children.setter
    def children(self, value: typing.List[ChildDict]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="orderedTags")
    def ordered_tags(self) -> OrderedStringSet:
        ...

    @ordered_tags.setter
    def ordered_tags(self, value: OrderedStringSet) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="orderedTagsForInitialization")
    def ordered_tags_for_initialization(self) -> OrderedStringSet:
        ...

    @ordered_tags_for_initialization.setter
    def ordered_tags_for_initialization(self, value: OrderedStringSet) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="orderedTagsForReplacement")
    def ordered_tags_for_replacement(self) -> OrderedStringSet:
        ...

    @ordered_tags_for_replacement.setter
    def ordered_tags_for_replacement(self, value: OrderedStringSet) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="parents")
    def parents(self) -> typing.List[typing.Union["Job", "JobCollection"]]:
        ...

    @parents.setter
    def parents(self, value: typing.List[typing.Union["Job", "JobCollection"]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="allowFailureForInitialization")
    def allow_failure_for_initialization(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]]:
        ...

    @allow_failure_for_initialization.setter
    def allow_failure_for_initialization(
        self,
        value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="allowFailureForReplacement")
    def allow_failure_for_replacement(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]]:
        ...

    @allow_failure_for_replacement.setter
    def allow_failure_for_replacement(
        self,
        value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Optional["Artifacts"]:
        ...

    @artifacts.setter
    def artifacts(self, value: typing.Optional["Artifacts"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="artifactsForInitialization")
    def artifacts_for_initialization(self) -> typing.Optional["Artifacts"]:
        ...

    @artifacts_for_initialization.setter
    def artifacts_for_initialization(self, value: typing.Optional["Artifacts"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="artifactsForReplacement")
    def artifacts_for_replacement(self) -> typing.Optional["Artifacts"]:
        ...

    @artifacts_for_replacement.setter
    def artifacts_for_replacement(self, value: typing.Optional["Artifacts"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> typing.Optional[Cache]:
        ...

    @cache.setter
    def cache(self, value: typing.Optional[Cache]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="cacheForInitialization")
    def cache_for_initialization(self) -> typing.Optional[Cache]:
        ...

    @cache_for_initialization.setter
    def cache_for_initialization(self, value: typing.Optional[Cache]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        ...

    @dependencies.setter
    def dependencies(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dependenciesForInitialization")
    def dependencies_for_initialization(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        ...

    @dependencies_for_initialization.setter
    def dependencies_for_initialization(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dependenciesForReplacement")
    def dependencies_for_replacement(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        ...

    @dependencies_for_replacement.setter
    def dependencies_for_replacement(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageForInitialization")
    def image_for_initialization(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, Image]]:
        ...

    @image_for_initialization.setter
    def image_for_initialization(
        self,
        value: typing.Optional[typing.Union[builtins.str, Image]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="imageForReplacement")
    def image_for_replacement(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, Image]]:
        ...

    @image_for_replacement.setter
    def image_for_replacement(
        self,
        value: typing.Optional[typing.Union[builtins.str, Image]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="needs")
    def needs(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        ...

    @needs.setter
    def needs(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="needsForInitialization")
    def needs_for_initialization(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        ...

    @needs_for_initialization.setter
    def needs_for_initialization(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="needsForReplacement")
    def needs_for_replacement(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        ...

    @needs_for_replacement.setter
    def needs_for_replacement(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rulesForInitialization")
    def rules_for_initialization(self) -> typing.Optional[typing.List[Rule]]:
        ...

    @rules_for_initialization.setter
    def rules_for_initialization(
        self,
        value: typing.Optional[typing.List[Rule]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rulesForReplacement")
    def rules_for_replacement(self) -> typing.Optional[typing.List[Rule]]:
        ...

    @rules_for_replacement.setter
    def rules_for_replacement(self, value: typing.Optional[typing.List[Rule]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rulesToAppend")
    def rules_to_append(self) -> typing.Optional[typing.List[Rule]]:
        ...

    @rules_to_append.setter
    def rules_to_append(self, value: typing.Optional[typing.List[Rule]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rulesToPrepend")
    def rules_to_prepend(self) -> typing.Optional[typing.List[Rule]]:
        ...

    @rules_to_prepend.setter
    def rules_to_prepend(self, value: typing.Optional[typing.List[Rule]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="scriptsToAppend")
    def scripts_to_append(self) -> typing.Optional[typing.List[builtins.str]]:
        ...

    @scripts_to_append.setter
    def scripts_to_append(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="scriptsToPrepend")
    def scripts_to_prepend(self) -> typing.Optional[typing.List[builtins.str]]:
        ...

    @scripts_to_prepend.setter
    def scripts_to_prepend(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @variables.setter
    def variables(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="variablesForInitialization")
    def variables_for_initialization(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @variables_for_initialization.setter
    def variables_for_initialization(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="variablesForReplacement")
    def variables_for_replacement(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @variables_for_replacement.setter
    def variables_for_replacement(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        ...

    @jsii.member(jsii_name="addChildren")
    def add_children(
        self,
        *,
        jobs_or_job_collections: typing.Sequence[typing.Union["Job", "JobCollection"]],
        name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> "JobCollection":
        '''Add ``gcix.Job``s or other ``gcix.JobCollection``s to this JobCollection.

        Adding a child creates a copy of that child. You should provide a name or
        stage when adding children, to make them different from other places
        where they will be used.

        :param jobs_or_job_collections: 
        :param name: 
        :param stage: 

        :return: JobCollection of the modified ``JobCollection`` object.
        '''
        ...

    @jsii.member(jsii_name="addParent")
    def add_parent(self, parent: "JobCollection") -> None:
        '''
        :param parent: -
        '''
        ...

    @jsii.member(jsii_name="initializeAllowFailure")
    def initialize_allow_failure(
        self,
        allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignAllowFailure()`` to all jobs within this JobCollection that haven't been set the allowFailure before.

        :param allow_failure: ???

        :return: the modified ``JobCollection`` object.
        '''
        ...

    @jsii.member(jsii_name="initializeArtifacts")
    def initialize_artifacts(self, artifacts: "Artifacts") -> "JobCollection":
        '''Sets ``gcix.Job.artifacts`` to all jobs within this JobCollection that haven't been set the artifacs before.

        :param artifacts: ???
        '''
        ...

    @jsii.member(jsii_name="initializeCache")
    def initialize_cache(self, cache: Cache) -> "JobCollection":
        '''Calling ``gcix.Job.assigneCache()`` to all jobs within this JobCollection that haven't been set the cache before.

        :param cache: ???
        '''
        ...

    @jsii.member(jsii_name="initializeDependencies")
    def initialize_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignDependencies()`` to all jobs within the first stage of this JobCollection that haven't been added dependencies before.

        An empty parameter list means that jobs will get an empty dependency
        list and thus does not download artifacts by default.

        :param dependencies: ???
        '''
        ...

    @jsii.member(jsii_name="initializeImage")
    def initialize_image(
        self,
        image: typing.Union[builtins.str, Image],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignImage()`` to all jobs within this JobCollection.

        :param image: ???
        '''
        ...

    @jsii.member(jsii_name="initializeNeeds")
    def initialize_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignNeeds()`` to all jobs within the first stage of this JobCollection that haven't been added needs before.

        An empty parameter list means that jobs will get an empty dependency
        list and thus does not depend on other jobs by default.

        :param needs: ???
        '''
        ...

    @jsii.member(jsii_name="initializeRules")
    def initialize_rules(self, rules: typing.Sequence[Rule]) -> "JobCollection":
        '''Calling ``gcix.Job.append_rules()`` to all jobs within this JobCollection that haven't been added rules before.

        :param rules: ???
        '''
        ...

    @jsii.member(jsii_name="initializeTags")
    def initialize_tags(self, tags: typing.Sequence[builtins.str]) -> "JobCollection":
        '''Calling ``gcix.Job.addTags([...])`` to all jobs within this JobCollection that haven't been added tags before.

        :param tags: ???
        '''
        ...

    @jsii.member(jsii_name="initializeVariables")
    def initialize_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.addVariables({...})`` to all jobs within this JobCollection that haven't been added variables before.

        :param variables: ???
        '''
        ...

    @jsii.member(jsii_name="overrideAllowFailure")
    def override_allow_failure(
        self,
        allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignAllowFailure()`` to all jobs within this JobCollection overriding any previous set value.

        :param allow_failure: ???

        :return: the modified ``JobCollection`` object.
        '''
        ...

    @jsii.member(jsii_name="overrideDependencies")
    def override_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignDependencies()`` to all jobs within the first stage of this JobCollection and overriding any previously added dependencies to that jobs.

        An empty parameter list means that jobs will get an empty dependency list
        and thus does not download artifacts.

        :param dependencies: ???
        '''
        ...

    @jsii.member(jsii_name="overrideImage")
    def override_image(
        self,
        image: typing.Union[builtins.str, Image],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignImage()`` to all jobs within this JobCollection overriding any previous set value.

        :param image: ???
        '''
        ...

    @jsii.member(jsii_name="overrideNeeds")
    def override_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignNeeds()`` to all jobs within the first stage of this JobCollection and overriding any previously added needs to that jobs.

        An empty parameter list means that jobs will get an empty dependency list
        and thus does not depend on other jobs.

        :param needs: ???
        '''
        ...

    @jsii.member(jsii_name="overrideRules")
    def override_rules(self, rules: typing.Sequence[Rule]) -> "JobCollection":
        '''Calling ``gcix.Job.overrideRules()`` to all jobs within this JobCollection and overriding any previously added rules to that jobs.

        :param rules: ???
        '''
        ...

    @jsii.member(jsii_name="overrideTags")
    def override_tags(self, tags: typing.Sequence[builtins.str]) -> "JobCollection":
        '''Calling ``gcix.Job.addTags([...])`` to all jobs within this JobCollection and overriding any previously added tags to that jobs.

        :param tags: ???
        '''
        ...

    @jsii.member(jsii_name="overrideVariables")
    def override_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.addVariables({...})`` to all jobs within this JobCollection and overriding any previously added variables to that jobs.

        :param variables: ???
        '''
        ...


class _IJobCollectionProxy(
    jsii.proxy_for(IJobCollectionBase), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@gcix/gcix.IJobCollection"

    @builtins.property
    @jsii.member(jsii_name="lastJobsExecuted")
    def last_jobs_executed(self) -> typing.List["Job"]:
        '''This property returns all Jobs from the last stage of this JobCollection.

        This is typically be requested from a job which has setup this
        JobCollection as need, to determine all actual jobs of this JobCollection
        as need.
        '''
        return typing.cast(typing.List["Job"], jsii.get(self, "lastJobsExecuted"))

    @builtins.property
    @jsii.member(jsii_name="nestedJobs")
    def nested_jobs(self) -> typing.List["Job"]:
        '''
        :return:

        all jobs of this this JobCollection as well as jobs of
        sub-JobCollection recursively.
        '''
        return typing.cast(typing.List["Job"], jsii.get(self, "nestedJobs"))

    @builtins.property
    @jsii.member(jsii_name="populatedJobs")
    def populated_jobs(self) -> typing.List["Job"]:
        '''Returns a list with populated copies of all nested jobs of this JobCollection.

        Populated means, that all attributes of a Job which depends on its context
        are resolved to their final values. The context is primarily the
        JobCollection within the jobs resides but also dependencies to other
        jobs and JobCollection's. Thus this JobCollection will apply its own
        configuration, like variables to add, tags to set, etc., to all its jobs
        and JobCollection's.

        Copies means what it says, that the returned job are not the same job
        objects, originally added to this JobCollection, but copies of them.

        Nested means, that also jobs from JobCollection's within this
        JobCollection, are returned, as well as jobs from JobCollection's within
        JobCollection's within this JobCollection and so on.
        '''
        return typing.cast(typing.List["Job"], jsii.get(self, "populatedJobs"))

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List[ChildDict]:
        return typing.cast(typing.List[ChildDict], jsii.get(self, "children"))

    @children.setter
    def children(self, value: typing.List[ChildDict]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce374c03318c12e49c9ccafdbc958569117f5dc171d0594c3551439750e0983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "children", value)

    @builtins.property
    @jsii.member(jsii_name="orderedTags")
    def ordered_tags(self) -> OrderedStringSet:
        return typing.cast(OrderedStringSet, jsii.get(self, "orderedTags"))

    @ordered_tags.setter
    def ordered_tags(self, value: OrderedStringSet) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bbb7310bbdbd6426286205b78849eadb3f2fddf66c55ff578788f0d8799f9d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderedTags", value)

    @builtins.property
    @jsii.member(jsii_name="orderedTagsForInitialization")
    def ordered_tags_for_initialization(self) -> OrderedStringSet:
        return typing.cast(OrderedStringSet, jsii.get(self, "orderedTagsForInitialization"))

    @ordered_tags_for_initialization.setter
    def ordered_tags_for_initialization(self, value: OrderedStringSet) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb114e52af4b58ffa72c76d15d44a685595ea11b02da3bb6b732e4728fc0fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderedTagsForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="orderedTagsForReplacement")
    def ordered_tags_for_replacement(self) -> OrderedStringSet:
        return typing.cast(OrderedStringSet, jsii.get(self, "orderedTagsForReplacement"))

    @ordered_tags_for_replacement.setter
    def ordered_tags_for_replacement(self, value: OrderedStringSet) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924fa58aa9f55459d00fa413efc595d87b8d63bb2dbac214b1529f96285d2b16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderedTagsForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="parents")
    def parents(self) -> typing.List[typing.Union["Job", "JobCollection"]]:
        return typing.cast(typing.List[typing.Union["Job", "JobCollection"]], jsii.get(self, "parents"))

    @parents.setter
    def parents(self, value: typing.List[typing.Union["Job", "JobCollection"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87380f08cd21392b245906f52afd056bb7bfc2b2df9b1c53ac84ba401d0cde1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parents", value)

    @builtins.property
    @jsii.member(jsii_name="allowFailureForInitialization")
    def allow_failure_for_initialization(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]]:
        return typing.cast(typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]], jsii.get(self, "allowFailureForInitialization"))

    @allow_failure_for_initialization.setter
    def allow_failure_for_initialization(
        self,
        value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4713420b5120162bd4c3efb9eb6a96e7b26cd0de808a786f3aa7a6ed7829f739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailureForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="allowFailureForReplacement")
    def allow_failure_for_replacement(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]]:
        return typing.cast(typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]], jsii.get(self, "allowFailureForReplacement"))

    @allow_failure_for_replacement.setter
    def allow_failure_for_replacement(
        self,
        value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d16c8e870a92ac208345b5ac5b9e57305f5f2b332da630c3adf973b22a8631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailureForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Optional["Artifacts"]:
        return typing.cast(typing.Optional["Artifacts"], jsii.get(self, "artifacts"))

    @artifacts.setter
    def artifacts(self, value: typing.Optional["Artifacts"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800e6fd839dba4dc782d83b6fe96b46aac96ca4ae90386bdc94fc2cb5fee4d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifacts", value)

    @builtins.property
    @jsii.member(jsii_name="artifactsForInitialization")
    def artifacts_for_initialization(self) -> typing.Optional["Artifacts"]:
        return typing.cast(typing.Optional["Artifacts"], jsii.get(self, "artifactsForInitialization"))

    @artifacts_for_initialization.setter
    def artifacts_for_initialization(self, value: typing.Optional["Artifacts"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5814f2b08c7a25d56ef31ed50b4a62a958b9acb5c65f827ca4745b5bacba1d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactsForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="artifactsForReplacement")
    def artifacts_for_replacement(self) -> typing.Optional["Artifacts"]:
        return typing.cast(typing.Optional["Artifacts"], jsii.get(self, "artifactsForReplacement"))

    @artifacts_for_replacement.setter
    def artifacts_for_replacement(self, value: typing.Optional["Artifacts"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1927e02979834ceb11c4218027e92f100e3a4ba08370df25772ced608cbb3fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactsForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> typing.Optional[Cache]:
        return typing.cast(typing.Optional[Cache], jsii.get(self, "cache"))

    @cache.setter
    def cache(self, value: typing.Optional[Cache]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165518ad606b6deaa654cafa77c1948747a3eeaa82478113ccbd5a371456d44b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cache", value)

    @builtins.property
    @jsii.member(jsii_name="cacheForInitialization")
    def cache_for_initialization(self) -> typing.Optional[Cache]:
        return typing.cast(typing.Optional[Cache], jsii.get(self, "cacheForInitialization"))

    @cache_for_initialization.setter
    def cache_for_initialization(self, value: typing.Optional[Cache]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4e060d038f6c70721ff5d4f44f7291da06b2e1a27c855479635c78c2e36bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]], jsii.get(self, "dependencies"))

    @dependencies.setter
    def dependencies(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d29466e344000e02a13dfa43165f522a87dc3cc60bf38de9c200c73fbda61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencies", value)

    @builtins.property
    @jsii.member(jsii_name="dependenciesForInitialization")
    def dependencies_for_initialization(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]], jsii.get(self, "dependenciesForInitialization"))

    @dependencies_for_initialization.setter
    def dependencies_for_initialization(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f35524c5b155c2bf7ba26231196e402225fbc2cbcc5e4e4edb6f645429e5ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependenciesForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="dependenciesForReplacement")
    def dependencies_for_replacement(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]], jsii.get(self, "dependenciesForReplacement"))

    @dependencies_for_replacement.setter
    def dependencies_for_replacement(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d67c8b1a9eda875c58e35e7cf2c724d2cb1ec6a34adf52d194fb242ece22c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependenciesForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="imageForInitialization")
    def image_for_initialization(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, Image]]:
        return typing.cast(typing.Optional[typing.Union[builtins.str, Image]], jsii.get(self, "imageForInitialization"))

    @image_for_initialization.setter
    def image_for_initialization(
        self,
        value: typing.Optional[typing.Union[builtins.str, Image]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437f18fccd4e9fbbc5dd6edfc97e247a393ec912b32b1e962024c7ec2a819f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="imageForReplacement")
    def image_for_replacement(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, Image]]:
        return typing.cast(typing.Optional[typing.Union[builtins.str, Image]], jsii.get(self, "imageForReplacement"))

    @image_for_replacement.setter
    def image_for_replacement(
        self,
        value: typing.Optional[typing.Union[builtins.str, Image]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed07e70cbdd86434500eac7b3844d882ec5dc29e83d145a7bad125a09836698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="needs")
    def needs(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]], jsii.get(self, "needs"))

    @needs.setter
    def needs(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3924c92afb045dc0f499a2c3f57bd234c45e6e35cce5bdaa5dc9a11b0d60c9de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "needs", value)

    @builtins.property
    @jsii.member(jsii_name="needsForInitialization")
    def needs_for_initialization(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]], jsii.get(self, "needsForInitialization"))

    @needs_for_initialization.setter
    def needs_for_initialization(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463f7c8632c746a867ae8963f6b7ecfce290f49308e20c117299f9f0b6435525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "needsForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="needsForReplacement")
    def needs_for_replacement(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]], jsii.get(self, "needsForReplacement"))

    @needs_for_replacement.setter
    def needs_for_replacement(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4c15a84c91915d015a98a495f261fe0bc292fd9556f2e2828541a4db83822a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "needsForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="rulesForInitialization")
    def rules_for_initialization(self) -> typing.Optional[typing.List[Rule]]:
        return typing.cast(typing.Optional[typing.List[Rule]], jsii.get(self, "rulesForInitialization"))

    @rules_for_initialization.setter
    def rules_for_initialization(
        self,
        value: typing.Optional[typing.List[Rule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b28a39469fca1a505c49931b555665f211be55c751f2f5f15042e6640a7c465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="rulesForReplacement")
    def rules_for_replacement(self) -> typing.Optional[typing.List[Rule]]:
        return typing.cast(typing.Optional[typing.List[Rule]], jsii.get(self, "rulesForReplacement"))

    @rules_for_replacement.setter
    def rules_for_replacement(self, value: typing.Optional[typing.List[Rule]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4f3c166a56a27f71302cc0e190965e0c21bc65aa0bdd2ec25087e139dfe5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="rulesToAppend")
    def rules_to_append(self) -> typing.Optional[typing.List[Rule]]:
        return typing.cast(typing.Optional[typing.List[Rule]], jsii.get(self, "rulesToAppend"))

    @rules_to_append.setter
    def rules_to_append(self, value: typing.Optional[typing.List[Rule]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f96572ea161c18f87c8389bbb82399236232bab6cd5bbf6abebde4ed1ea2ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesToAppend", value)

    @builtins.property
    @jsii.member(jsii_name="rulesToPrepend")
    def rules_to_prepend(self) -> typing.Optional[typing.List[Rule]]:
        return typing.cast(typing.Optional[typing.List[Rule]], jsii.get(self, "rulesToPrepend"))

    @rules_to_prepend.setter
    def rules_to_prepend(self, value: typing.Optional[typing.List[Rule]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cccb9df8e4dec5431a67a3efb3c5b68359970e910c8b4848395078ca1ee8cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesToPrepend", value)

    @builtins.property
    @jsii.member(jsii_name="scriptsToAppend")
    def scripts_to_append(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scriptsToAppend"))

    @scripts_to_append.setter
    def scripts_to_append(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e5b1c45f75b4231f79550e1a3aa2a451598f07f90dc5c1370b112d6bb30bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptsToAppend", value)

    @builtins.property
    @jsii.member(jsii_name="scriptsToPrepend")
    def scripts_to_prepend(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scriptsToPrepend"))

    @scripts_to_prepend.setter
    def scripts_to_prepend(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7ce1bc9adfe77dce0846ffd4bfbb42c00c6a5461cef05959a206ab95e2cc95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptsToPrepend", value)

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variables"))

    @variables.setter
    def variables(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ba53eb89a1220b77e8d246920f5d1d493e011367d63af1c3f59cbd5a54dc0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variables", value)

    @builtins.property
    @jsii.member(jsii_name="variablesForInitialization")
    def variables_for_initialization(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variablesForInitialization"))

    @variables_for_initialization.setter
    def variables_for_initialization(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dba70304a311fbb2a0bce9781b2b335896e010b7f432d113d52137d6f5e5c670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variablesForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="variablesForReplacement")
    def variables_for_replacement(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variablesForReplacement"))

    @variables_for_replacement.setter
    def variables_for_replacement(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620af3bad665631d9118208b10f6e2c10f078d1dd147228dadcdbe679ecc8025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variablesForReplacement", value)

    @jsii.member(jsii_name="addChildren")
    def add_children(
        self,
        *,
        jobs_or_job_collections: typing.Sequence[typing.Union["Job", "JobCollection"]],
        name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> "JobCollection":
        '''Add ``gcix.Job``s or other ``gcix.JobCollection``s to this JobCollection.

        Adding a child creates a copy of that child. You should provide a name or
        stage when adding children, to make them different from other places
        where they will be used.

        :param jobs_or_job_collections: 
        :param name: 
        :param stage: 

        :return: JobCollection of the modified ``JobCollection`` object.
        '''
        props = AddChildrenProps(
            jobs_or_job_collections=jobs_or_job_collections, name=name, stage=stage
        )

        return typing.cast("JobCollection", jsii.invoke(self, "addChildren", [props]))

    @jsii.member(jsii_name="addParent")
    def add_parent(self, parent: "JobCollection") -> None:
        '''
        :param parent: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03777d712d99eca1625438ac0f95a7fe10768d5338c879c44c7398ac9f6ea504)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
        return typing.cast(None, jsii.invoke(self, "addParent", [parent]))

    @jsii.member(jsii_name="initializeAllowFailure")
    def initialize_allow_failure(
        self,
        allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignAllowFailure()`` to all jobs within this JobCollection that haven't been set the allowFailure before.

        :param allow_failure: ???

        :return: the modified ``JobCollection`` object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5387c850358faf7f706c15e46d31610050877fb3d21e61e87ab9e1b37d342a71)
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeAllowFailure", [allow_failure]))

    @jsii.member(jsii_name="initializeArtifacts")
    def initialize_artifacts(self, artifacts: "Artifacts") -> "JobCollection":
        '''Sets ``gcix.Job.artifacts`` to all jobs within this JobCollection that haven't been set the artifacs before.

        :param artifacts: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a97e83dc7ff8a14d0c568ac16545b1bb57a722286a5426e5ad67a752d5214b)
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeArtifacts", [artifacts]))

    @jsii.member(jsii_name="initializeCache")
    def initialize_cache(self, cache: Cache) -> "JobCollection":
        '''Calling ``gcix.Job.assigneCache()`` to all jobs within this JobCollection that haven't been set the cache before.

        :param cache: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0181c42295494c9b48c2e4c414b843abb6fb34e9517474823787ce2525a1781)
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeCache", [cache]))

    @jsii.member(jsii_name="initializeDependencies")
    def initialize_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignDependencies()`` to all jobs within the first stage of this JobCollection that haven't been added dependencies before.

        An empty parameter list means that jobs will get an empty dependency
        list and thus does not download artifacts by default.

        :param dependencies: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9aa08b460359399ef73f771713288180f56d37fa2fc473735b6e3062eddff2b)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeDependencies", [dependencies]))

    @jsii.member(jsii_name="initializeImage")
    def initialize_image(
        self,
        image: typing.Union[builtins.str, Image],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignImage()`` to all jobs within this JobCollection.

        :param image: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc9cb4619acadea11cc54e7e8e11e287580fd542190c2311ecbe6297088069c5)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeImage", [image]))

    @jsii.member(jsii_name="initializeNeeds")
    def initialize_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignNeeds()`` to all jobs within the first stage of this JobCollection that haven't been added needs before.

        An empty parameter list means that jobs will get an empty dependency
        list and thus does not depend on other jobs by default.

        :param needs: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2cb512fd29fb38c1fd29b00d52a5029ecab4e4fc0060c1a73eda98718e3099)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeNeeds", [needs]))

    @jsii.member(jsii_name="initializeRules")
    def initialize_rules(self, rules: typing.Sequence[Rule]) -> "JobCollection":
        '''Calling ``gcix.Job.append_rules()`` to all jobs within this JobCollection that haven't been added rules before.

        :param rules: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503b25afaad5b3a95023281da352be04b22dc753f0badcc3a707591d9ab35ab5)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeRules", [rules]))

    @jsii.member(jsii_name="initializeTags")
    def initialize_tags(self, tags: typing.Sequence[builtins.str]) -> "JobCollection":
        '''Calling ``gcix.Job.addTags([...])`` to all jobs within this JobCollection that haven't been added tags before.

        :param tags: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58148eded3196a8d1778f4f7a689f88b4ac1698f0b59f294e1fa028c54d6acc5)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeTags", [tags]))

    @jsii.member(jsii_name="initializeVariables")
    def initialize_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.addVariables({...})`` to all jobs within this JobCollection that haven't been added variables before.

        :param variables: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e713143f5860e1bbebec8cf9f48b9faade58bdf769d329049fd1c7c17f528cf)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeVariables", [variables]))

    @jsii.member(jsii_name="overrideAllowFailure")
    def override_allow_failure(
        self,
        allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignAllowFailure()`` to all jobs within this JobCollection overriding any previous set value.

        :param allow_failure: ???

        :return: the modified ``JobCollection`` object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de206756d2c823c2bcfef0d2825f3b535dcff8fc0456e0ba7ced9d307bfd9d4)
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideAllowFailure", [allow_failure]))

    @jsii.member(jsii_name="overrideDependencies")
    def override_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignDependencies()`` to all jobs within the first stage of this JobCollection and overriding any previously added dependencies to that jobs.

        An empty parameter list means that jobs will get an empty dependency list
        and thus does not download artifacts.

        :param dependencies: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b867e206d8134a599be691d8340c9613ecfd2eeec79c732f2458dc5af93625)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideDependencies", [dependencies]))

    @jsii.member(jsii_name="overrideImage")
    def override_image(
        self,
        image: typing.Union[builtins.str, Image],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignImage()`` to all jobs within this JobCollection overriding any previous set value.

        :param image: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2894761e19594ae15c6d28747a74a7790e903da192f64884c854acea95d180)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideImage", [image]))

    @jsii.member(jsii_name="overrideNeeds")
    def override_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignNeeds()`` to all jobs within the first stage of this JobCollection and overriding any previously added needs to that jobs.

        An empty parameter list means that jobs will get an empty dependency list
        and thus does not depend on other jobs.

        :param needs: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab56faa06054c66095bbea7ce370e78145d0d1b9b759c05d48d75b21579510dd)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideNeeds", [needs]))

    @jsii.member(jsii_name="overrideRules")
    def override_rules(self, rules: typing.Sequence[Rule]) -> "JobCollection":
        '''Calling ``gcix.Job.overrideRules()`` to all jobs within this JobCollection and overriding any previously added rules to that jobs.

        :param rules: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec78f97b536b9bd1e9abe68d46985468f4c1b546ea63925c5b54d7d29758c087)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideRules", [rules]))

    @jsii.member(jsii_name="overrideTags")
    def override_tags(self, tags: typing.Sequence[builtins.str]) -> "JobCollection":
        '''Calling ``gcix.Job.addTags([...])`` to all jobs within this JobCollection and overriding any previously added tags to that jobs.

        :param tags: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b300cdc454d508866352523585ce60b65f470797886b0fd1265c71a53c53a8a9)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideTags", [tags]))

    @jsii.member(jsii_name="overrideVariables")
    def override_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.addVariables({...})`` to all jobs within this JobCollection and overriding any previously added variables to that jobs.

        :param variables: ???
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9b96730d3dc815593bd4221cda8585e45d579a28c3537bf882917ad3457b84)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideVariables", [variables]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJobCollection).__jsii_proxy_class__ = lambda : _IJobCollectionProxy


@jsii.implements(IJob)
class Job(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.Job"):
    '''This class represents the Gitlab CI `Job <https://docs.gitlab.com/ee/ci/yaml/README.html#job-keywords>`_.'''

    def __init__(
        self,
        *,
        scripts: typing.Sequence[builtins.str],
        allow_failure: typing.Optional[typing.Union[builtins.bool, typing.Sequence[jsii.Number]]] = None,
        artifacts: typing.Optional["Artifacts"] = None,
        cache: typing.Optional[Cache] = None,
        dependencies: typing.Optional[typing.Sequence[typing.Union["Job", "JobCollection"]]] = None,
        image: typing.Optional[typing.Union[builtins.str, Image]] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[typing.Union["Job", "JobCollection", Need]]] = None,
        rules: typing.Optional[typing.Sequence[Rule]] = None,
        stage: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scripts: 
        :param allow_failure: 
        :param artifacts: 
        :param cache: 
        :param dependencies: 
        :param image: 
        :param name: 
        :param needs: 
        :param rules: 
        :param stage: 
        :param tags: 
        :param variables: 
        '''
        props = JobProps(
            scripts=scripts,
            allow_failure=allow_failure,
            artifacts=artifacts,
            cache=cache,
            dependencies=dependencies,
            image=image,
            name=name,
            needs=needs,
            rules=rules,
            stage=stage,
            tags=tags,
            variables=variables,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addDependencies")
    def add_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "Job":
        '''
        :param dependencies: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a48c4d96775cb493b2af94f11cdc8d7ceb50c61ab3b14ad8854081299da1bfe)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("Job", jsii.invoke(self, "addDependencies", [dependencies]))

    @jsii.member(jsii_name="addNeeds")
    def add_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "Job":
        '''
        :param needs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9ed914133e31f69e8796ec059fd9bde69e514367ca54cfe9094376557e60a1)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("Job", jsii.invoke(self, "addNeeds", [needs]))

    @jsii.member(jsii_name="addParent")
    def add_parent(self, parent: typing.Union["Job", "JobCollection"]) -> None:
        '''This method is called by ``gcix.JobCollection``s when the job is added to that JobCollection.

        The job needs to know its parents when ``getAllInstanceNames()`` is called.

        :param parent: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24fc1c24582c615ad8068c1095c83c5c03e52797bb6bd8a8d47bd2a7ab61107)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
        return typing.cast(None, jsii.invoke(self, "addParent", [parent]))

    @jsii.member(jsii_name="addTags")
    def add_tags(self, tags: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param tags: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a497289f09f740c75644ac694138b800021e4b73beb111933ed7cc2bf5cdc02c)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("Job", jsii.invoke(self, "addTags", [tags]))

    @jsii.member(jsii_name="addVariables")
    def add_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "Job":
        '''
        :param variables: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa6a8f7c0e607dc2f9e942f39f5f8ad964d6e4f7d906954e89d16169e45b028)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("Job", jsii.invoke(self, "addVariables", [variables]))

    @jsii.member(jsii_name="appendRules")
    def append_rules(self, rules: typing.Sequence[Rule]) -> "Job":
        '''
        :param rules: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1987c954bc8ff5f11f9b443debf9425852cfee535f0e85d2b79989d428923cf6)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("Job", jsii.invoke(self, "appendRules", [rules]))

    @jsii.member(jsii_name="appendScripts")
    def append_scripts(self, scripts: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param scripts: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125ab86f0029dcc67ca976ed83fa6db9e9404542d8cae4552e0d4dac0e9891f1)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        return typing.cast("Job", jsii.invoke(self, "appendScripts", [scripts]))

    @jsii.member(jsii_name="assignAllowFailure")
    def assign_allow_failure(
        self,
        allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
    ) -> "Job":
        '''
        :param allow_failure: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b23de588de9113dab19ef636449def6cb85f01d84a1a3b15ddf5e35a1b9a189)
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
        return typing.cast("Job", jsii.invoke(self, "assignAllowFailure", [allow_failure]))

    @jsii.member(jsii_name="assignArtifacts")
    def assign_artifacts(self, artifacts: "Artifacts") -> "Job":
        '''
        :param artifacts: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4b1d5e688c342aae8b3c5ca41e455b0b73d2c4ead55c8d858977d661f7cc2e)
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
        return typing.cast("Job", jsii.invoke(self, "assignArtifacts", [artifacts]))

    @jsii.member(jsii_name="assignCache")
    def assign_cache(self, cache: Cache) -> "Job":
        '''
        :param cache: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b56c55fca73e926648c394ffe52d09ce5bf6e1c066cf53a2c4f6f23a8da51e3)
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
        return typing.cast("Job", jsii.invoke(self, "assignCache", [cache]))

    @jsii.member(jsii_name="assignDependencies")
    def assign_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "Job":
        '''
        :param dependencies: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e49587b212e79c7a8106b2f2a7ca2e46934c763da19022c7f2a8e64400b0a6a)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("Job", jsii.invoke(self, "assignDependencies", [dependencies]))

    @jsii.member(jsii_name="assignImage")
    def assign_image(self, image: typing.Union[builtins.str, Image]) -> "Job":
        '''Sets the image of this job.

        For a simple container image you can provide the origin of the image.
        If you want to set the entrypoint, you have to provide an Image object instead.

        !! Any previous values will be overwritten.

        :param image: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71deea21d7c27e527b77b8214aafa016d473c5807479aa2efc7d865ef86e07ec)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast("Job", jsii.invoke(self, "assignImage", [image]))

    @jsii.member(jsii_name="assignNeeds")
    def assign_needs(
        self,
        needs: typing.Sequence[typing.Union["Job", "JobCollection", Need]],
    ) -> "Job":
        '''
        :param needs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40732962652fe2e50d84e53ff922a3dbd8633c1b598ff35d7e393bd6c5786ab2)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("Job", jsii.invoke(self, "assignNeeds", [needs]))

    @jsii.member(jsii_name="assignTags")
    def assign_tags(self, tags: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param tags: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb5e14b00eb4e350b88ab4d9f6009226dc17d1e2e8058bca298f098fd88bdca)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("Job", jsii.invoke(self, "assignTags", [tags]))

    @jsii.member(jsii_name="copy")
    def copy(self) -> "Job":
        '''Returns an independent, deep copy object of this job.'''
        return typing.cast("Job", jsii.invoke(self, "copy", []))

    @jsii.member(jsii_name="extendName")
    def extend_name(self, name: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs name.

        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f112eb86517c848f04a124efbfe5ad1a61a77053011ed534cbd62b0298f2ef4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "extendName", [name]))

    @jsii.member(jsii_name="extendStage")
    def extend_stage(self, stage: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs name and stage.

        :param stage: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f79da5bb710007e93b0622bb0ca050c33ffe1c2ba0165ae82cf3ba104205ef5)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast(None, jsii.invoke(self, "extendStage", [stage]))

    @jsii.member(jsii_name="extendStageValue")
    def extend_stage_value(self, stage: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs stage.

        :param stage: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3114d3274dade702f3ea59163b7093cf963a0fc0f5b52deb9548ed497c192006)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast(None, jsii.invoke(self, "extendStageValue", [stage]))

    @jsii.member(jsii_name="getAllInstanceNames")
    def get_all_instance_names(
        self,
        child: typing.Optional[typing.Union["Job", "JobCollection"]] = None,
    ) -> OrderedStringSet:
        '''Return all instance names from the given child.

        That means all combinations of the childs name and stage within this
        sequence and all parent sequences.

        :param child: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940f39ed0563dbd5ce1ddd0196a7f0371b0086ce42e8bd3fe034a0b870629473)
            check_type(argname="argument child", value=child, expected_type=type_hints["child"])
        return typing.cast(OrderedStringSet, jsii.invoke(self, "getAllInstanceNames", [child]))

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f410058ae45f87b4744967f654f53c1d4767ecb5a4860e4e045449a2280260bb)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="prependRules")
    def prepend_rules(self, rules: typing.Sequence[Rule]) -> "Job":
        '''
        :param rules: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ab7c7bc8d431b6232632429642a5cb932bd7d10f424185811fffcce0247f83)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("Job", jsii.invoke(self, "prependRules", [rules]))

    @jsii.member(jsii_name="prependScripts")
    def prepend_scripts(self, scripts: typing.Sequence[builtins.str]) -> "Job":
        '''
        :param scripts: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0ca5bc0e4528b7bf578f909d4c3803e4cb3ba77468906396de9cd5fa3e77c7)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        return typing.cast("Job", jsii.invoke(self, "prependScripts", [scripts]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        '''Getter method to receive added tags.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="allowFailure")
    def allow_failure(
        self,
    ) -> typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]:
        return typing.cast(typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]], jsii.get(self, "allowFailure"))

    @allow_failure.setter
    def allow_failure(
        self,
        value: typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0935cd0552d340f972384e3a86ae9d10ddff13b42b30dd00d9084f480a351c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailure", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbdccd2312ed9afe38e1f999efa8e87afb00bf1172a779a57d7bf542f10ef02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="orderedTags")
    def ordered_tags(self) -> OrderedStringSet:
        return typing.cast(OrderedStringSet, jsii.get(self, "orderedTags"))

    @ordered_tags.setter
    def ordered_tags(self, value: OrderedStringSet) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4593026978879fa34fbe85bf848f401a835148b38891be402dd99c6446a6a6bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderedTags", value)

    @builtins.property
    @jsii.member(jsii_name="parents")
    def parents(self) -> typing.List[typing.Union["Job", "JobCollection"]]:
        return typing.cast(typing.List[typing.Union["Job", "JobCollection"]], jsii.get(self, "parents"))

    @parents.setter
    def parents(self, value: typing.List[typing.Union["Job", "JobCollection"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__464e10f1bf91d67d20ccb380dc46d815aa1e5ef0a935f7f0264179dadc1a4c35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parents", value)

    @builtins.property
    @jsii.member(jsii_name="scripts")
    def scripts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scripts"))

    @scripts.setter
    def scripts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5171ff36feb8db472dcbfe085f15b589f28a5ae6e733efdabea54894d36f9b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scripts", value)

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stage"))

    @stage.setter
    def stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819b52d69443a5cfcf420e16e85c1df5ccaf9582385505b81b81a0b71b20c178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value)

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Optional["Artifacts"]:
        return typing.cast(typing.Optional["Artifacts"], jsii.get(self, "artifacts"))

    @artifacts.setter
    def artifacts(self, value: typing.Optional["Artifacts"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a7abfd01c3c0481e3e95bf716cbcb98b2cac85ee4aa21ac4b14b431b005c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifacts", value)

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> typing.Optional[Cache]:
        return typing.cast(typing.Optional[Cache], jsii.get(self, "cache"))

    @cache.setter
    def cache(self, value: typing.Optional[Cache]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed9076a7ea726084ecfe53ccd2393796875750aab4677a9d334c0522cd3441d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cache", value)

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]], jsii.get(self, "dependencies"))

    @dependencies.setter
    def dependencies(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a5088a4d42d248dff0b622ba0653ee40968fd45e106d98b40c27e729d46cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencies", value)

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> typing.Optional[Image]:
        return typing.cast(typing.Optional[Image], jsii.get(self, "image"))

    @image.setter
    def image(self, value: typing.Optional[Image]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fea17d587e11eaa0a2f770acaa9f2ac1e06dfbcc89e0755f32ca9c27b9e860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value)

    @builtins.property
    @jsii.member(jsii_name="needs")
    def needs(
        self,
    ) -> typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]], jsii.get(self, "needs"))

    @needs.setter
    def needs(
        self,
        value: typing.Optional[typing.List[typing.Union["Job", "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26404ef55b583b637a848e06f3ef983eab5000ac5e9d19c79e43f35c8efb3e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "needs", value)

    @builtins.property
    @jsii.member(jsii_name="original")
    def original(self) -> typing.Optional["Job"]:
        return typing.cast(typing.Optional["Job"], jsii.get(self, "original"))

    @original.setter
    def original(self, value: typing.Optional["Job"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d69ee4b1126a9e6b9d9a678b8b768fc552ab7dde70643963bdef041c4578ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "original", value)

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> typing.Optional[typing.List[Rule]]:
        return typing.cast(typing.Optional[typing.List[Rule]], jsii.get(self, "rules"))

    @rules.setter
    def rules(self, value: typing.Optional[typing.List[Rule]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2609118cc722fb49976ac188e0bb7aea933f6aa6008140e228266700022786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value)

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variables"))

    @variables.setter
    def variables(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa0c5b49599722d0311be14500175639c97eb43d99da3f0b00e5e9eb6e8c6a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variables", value)


@jsii.implements(IJobCollection)
class JobCollection(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.JobCollection"):
    '''A JobCollection collects multiple ``gcix.Job``s and/or other ``gcix.JobCollection``s into a group.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addChildren")
    def add_children(
        self,
        *,
        jobs_or_job_collections: typing.Sequence[typing.Union[Job, "JobCollection"]],
        name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> "JobCollection":
        '''Add ``gcix.Job``s or other ``gcix.JobCollection``s to this JobCollection.

        Adding a child creates a copy of that child. You should provide a name or
        stage when adding children, to make them different from other places
        where they will be used.

        :param jobs_or_job_collections: 
        :param name: 
        :param stage: 
        '''
        props = AddChildrenProps(
            jobs_or_job_collections=jobs_or_job_collections, name=name, stage=stage
        )

        return typing.cast("JobCollection", jsii.invoke(self, "addChildren", [props]))

    @jsii.member(jsii_name="addDependencies")
    def add_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union[Job, "JobCollection", Need]],
    ) -> "JobCollection":
        '''
        :param dependencies: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42da1733be21c876f2b8c557056190aa08f5c8fe3d1d8ae2c892478c8b25944d)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("JobCollection", jsii.invoke(self, "addDependencies", [dependencies]))

    @jsii.member(jsii_name="addNeeds")
    def add_needs(
        self,
        needs: typing.Sequence[typing.Union[Job, "JobCollection", Need]],
    ) -> "JobCollection":
        '''
        :param needs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c8f44da804e65c760463d8598c8e5c4ad74285db44713758a3b34104758992)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("JobCollection", jsii.invoke(self, "addNeeds", [needs]))

    @jsii.member(jsii_name="addParent")
    def add_parent(self, parent: "JobCollection") -> None:
        '''
        :param parent: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a15c38332229518ae3150574e93608d030bdc56267bdb62254816ea300c990)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
        return typing.cast(None, jsii.invoke(self, "addParent", [parent]))

    @jsii.member(jsii_name="addTags")
    def add_tags(self, tags: typing.Sequence[builtins.str]) -> "JobCollection":
        '''
        :param tags: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f23d98dda585479188e9dcbdd461fcd8989bdb00710a83b9d000bc890223b3)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("JobCollection", jsii.invoke(self, "addTags", [tags]))

    @jsii.member(jsii_name="addVariables")
    def add_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "JobCollection":
        '''
        :param variables: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a07aedddf02b4327d2459c465db8d2c56c742db3d6be14c0627a083ece1600)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("JobCollection", jsii.invoke(self, "addVariables", [variables]))

    @jsii.member(jsii_name="appendRules")
    def append_rules(self, rules: typing.Sequence[Rule]) -> "JobCollection":
        '''
        :param rules: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8441a024959b5e13a0a59ff2c6c8fc8e59987261a6d2f920a02e78d3c2795e58)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("JobCollection", jsii.invoke(self, "appendRules", [rules]))

    @jsii.member(jsii_name="appendScripts")
    def append_scripts(self, scripts: typing.Sequence[builtins.str]) -> "JobCollection":
        '''
        :param scripts: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4b8070cd7a2d395a2395131f4d5026555f79f0003e4704e9fcad66ce05342e)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        return typing.cast("JobCollection", jsii.invoke(self, "appendScripts", [scripts]))

    @jsii.member(jsii_name="assignArtifacts")
    def assign_artifacts(self, artifacts: "Artifacts") -> "JobCollection":
        '''
        :param artifacts: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9462d9397982b304d6845e6a714d38a0271b5f25aa7ae896abb85e84a9ded523)
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
        return typing.cast("JobCollection", jsii.invoke(self, "assignArtifacts", [artifacts]))

    @jsii.member(jsii_name="assignCache")
    def assign_cache(self, cache: Cache) -> "JobCollection":
        '''
        :param cache: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c5e603d29cd58ae28e444f54de04c88cd13615c3fbc543a1fe6cdae3072da1)
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
        return typing.cast("JobCollection", jsii.invoke(self, "assignCache", [cache]))

    @jsii.member(jsii_name="getAllInstanceNames")
    def get_all_instance_names(
        self,
        child: typing.Optional[typing.Union[Job, "JobCollection"]] = None,
    ) -> OrderedStringSet:
        '''Return all instance names from the given child.

        That means all combinations of the childs name and stage within this
        JobCollection and all parent JobCollection's.

        :param child: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35258a06eebe532433381d99683b8ce812e15b851b60b783cb65f50888732928)
            check_type(argname="argument child", value=child, expected_type=type_hints["child"])
        return typing.cast(OrderedStringSet, jsii.invoke(self, "getAllInstanceNames", [child]))

    @jsii.member(jsii_name="initializeAllowFailure")
    def initialize_allow_failure(
        self,
        allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignAllowFailure()`` to all jobs within this JobCollection that haven't been set the allowFailure before.

        :param allow_failure: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed926c1e7c701a185debe51e9806aeb4c1f344d71504a252f886b065b267368e)
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeAllowFailure", [allow_failure]))

    @jsii.member(jsii_name="initializeArtifacts")
    def initialize_artifacts(self, artifacts: "Artifacts") -> "JobCollection":
        '''Sets ``gcix.Job.artifacts`` to all jobs within this JobCollection that haven't been set the artifacs before.

        :param artifacts: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de279575d6dfb45a6aa28c525f13751bb58d5d5f8c03225d5b98036a21d40bcc)
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeArtifacts", [artifacts]))

    @jsii.member(jsii_name="initializeCache")
    def initialize_cache(self, cache: Cache) -> "JobCollection":
        '''Calling ``gcix.Job.assigneCache()`` to all jobs within this JobCollection that haven't been set the cache before.

        :param cache: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338234c7a7d17c90c76c5eda5a4f4676850ddc78c0a35e52112a5f324519dc9e)
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeCache", [cache]))

    @jsii.member(jsii_name="initializeDependencies")
    def initialize_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union[Job, "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignDependencies()`` to all jobs within the first stage of this JobCollection that haven't been added dependencies before.

        An empty parameter list means that jobs will get an empty dependency
        list and thus does not download artifacts by default.

        :param dependencies: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb945393a73d8958d3fc4a5d8fe0b05468aeb7a896e1fd0c9280865d2bcbe97)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeDependencies", [dependencies]))

    @jsii.member(jsii_name="initializeImage")
    def initialize_image(
        self,
        image: typing.Union[builtins.str, Image],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignImage()`` to all jobs within this JobCollection.

        :param image: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc24cbfab1244ecb3fd94133029125b3dcf29d6d1b147b9f5f7e3937024ba6b4)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeImage", [image]))

    @jsii.member(jsii_name="initializeNeeds")
    def initialize_needs(
        self,
        needs: typing.Sequence[typing.Union[Job, "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignNeeds()`` to all jobs within the first stage of this JobCollection that haven't been added needs before.

        An empty parameter list means that jobs will get an empty dependency
        list and thus does not depend on other jobs by default.

        :param needs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fcd9a86bbbad45ce6aaa39fbfac2fb23ede7eae9c6cc49b0dde140061288059)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeNeeds", [needs]))

    @jsii.member(jsii_name="initializeRules")
    def initialize_rules(self, rules: typing.Sequence[Rule]) -> "JobCollection":
        '''Calling ``gcix.Job.append_rules()`` to all jobs within this JobCollection that haven't been added rules before.

        :param rules: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea4cbe17163697871c2357e3ff5231b092f24931fd8770f8894b2ff56d0daac)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeRules", [rules]))

    @jsii.member(jsii_name="initializeTags")
    def initialize_tags(self, tags: typing.Sequence[builtins.str]) -> "JobCollection":
        '''Calling ``gcix.Job.addTags([...])`` to all jobs within this JobCollection that haven't been added tags before.

        :param tags: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8fd49bc5a9330d7eff9194f17fe23ab926d47e5f632e1f9e61b4e1dcc45d46)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeTags", [tags]))

    @jsii.member(jsii_name="initializeVariables")
    def initialize_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.addVariables({...})`` to all jobs within this JobCollection that haven't been added variables before.

        :param variables: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88535091b1345fc77ff978fccb39ce8e9628c0cdd4f16fbc03c571b514065b14)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("JobCollection", jsii.invoke(self, "initializeVariables", [variables]))

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e90fdcf5ced3e3d3a71ffbec40dcc7c8c9e7c4039d0a74018ebb458e61485ce)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="overrideAllowFailure")
    def override_allow_failure(
        self,
        allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignAllowFailure()`` to all jobs within this JobCollection overriding any previous set value.

        :param allow_failure: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4884ab7cddd84ab13fd45721fecaa391483e6bae522d2a4fdec42b85937fab17)
            check_type(argname="argument allow_failure", value=allow_failure, expected_type=type_hints["allow_failure"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideAllowFailure", [allow_failure]))

    @jsii.member(jsii_name="overrideDependencies")
    def override_dependencies(
        self,
        dependencies: typing.Sequence[typing.Union[Job, "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignDependencies()`` to all jobs within the first stage of this JobCollection and overriding any previously added dependencies to that jobs.

        An empty parameter list means that jobs will get an empty dependency list
        and thus does not download artifacts.

        :param dependencies: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4638838c6c80a29aaabd27696ad3046a51855ae24e34b0b3c8440a96d369877c)
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideDependencies", [dependencies]))

    @jsii.member(jsii_name="overrideImage")
    def override_image(
        self,
        image: typing.Union[builtins.str, Image],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignImage()`` to all jobs within this JobCollection overriding any previous set value.

        :param image: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d78465bbcbf46c0e9f9b3c8b79e81b590a2e8490887d2a0031b33c4db024825)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideImage", [image]))

    @jsii.member(jsii_name="overrideNeeds")
    def override_needs(
        self,
        needs: typing.Sequence[typing.Union[Job, "JobCollection", Need]],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.assignNeeds()`` to all jobs within the first stage of this JobCollection and overriding any previously added needs to that jobs.

        An empty parameter list means that jobs will get an empty dependency list
        and thus does not depend on other jobs.

        :param needs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0134a14b49fa583bc5722071b32e2238e1151a607223bbe99189cf1edf4da56)
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideNeeds", [needs]))

    @jsii.member(jsii_name="overrideRules")
    def override_rules(self, rules: typing.Sequence[Rule]) -> "JobCollection":
        '''Calling ``gcix.Job.overrideRules()`` to all jobs within this JobCollection and overriding any previously added rules to that jobs.

        :param rules: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04261ac203124b3d169d4d239d34a7d547f8f8e46f5512c85dc2d2f74727996)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideRules", [rules]))

    @jsii.member(jsii_name="overrideTags")
    def override_tags(self, tags: typing.Sequence[builtins.str]) -> "JobCollection":
        '''Calling ``gcix.Job.addTags([...])`` to all jobs within this JobCollection and overriding any previously added tags to that jobs.

        :param tags: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d671ef71d13884eeb0dffbed3f512183dca07312902be0ec185079b1ea8a6efd)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideTags", [tags]))

    @jsii.member(jsii_name="overrideVariables")
    def override_variables(
        self,
        variables: typing.Mapping[builtins.str, builtins.str],
    ) -> "JobCollection":
        '''Calling ``gcix.Job.addVariables({...})`` to all jobs within this JobCollection and overriding any previously added variables to that jobs.

        :param variables: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb5530dd15a5924655ede8b1e1884af69bae49fdd77051ac3c4b35d44306157)
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        return typing.cast("JobCollection", jsii.invoke(self, "overrideVariables", [variables]))

    @jsii.member(jsii_name="prependRules")
    def prepend_rules(self, rules: typing.Sequence[Rule]) -> "JobCollection":
        '''
        :param rules: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5c159d9c5e4c27812c3da4dc97e6e56d1d584af158a50d7b0f284387c7260f)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        return typing.cast("JobCollection", jsii.invoke(self, "prependRules", [rules]))

    @jsii.member(jsii_name="prependScripts")
    def prepend_scripts(
        self,
        scripts: typing.Sequence[builtins.str],
    ) -> "JobCollection":
        '''
        :param scripts: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7df33f7e535655d2add62cf2ad779e256126fbbd1b9a2b3e9f6080b23ed4447)
            check_type(argname="argument scripts", value=scripts, expected_type=type_hints["scripts"])
        return typing.cast("JobCollection", jsii.invoke(self, "prependScripts", [scripts]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="lastJobsExecuted")
    def last_jobs_executed(self) -> typing.List[Job]:
        '''This property returns all Jobs from the last stage of this JobCollection.

        This is typically be requested from a job which has setup this
        JobCollection as need, to determine all actual jobs of this JobCollection
        as need.
        '''
        return typing.cast(typing.List[Job], jsii.get(self, "lastJobsExecuted"))

    @builtins.property
    @jsii.member(jsii_name="nestedJobs")
    def nested_jobs(self) -> typing.List[Job]:
        return typing.cast(typing.List[Job], jsii.get(self, "nestedJobs"))

    @builtins.property
    @jsii.member(jsii_name="populatedJobs")
    def populated_jobs(self) -> typing.List[Job]:
        '''Returns a list with populated copies of all nested jobs of this JobCollection.

        Populated means, that all attributes of a Job which depends on its context
        are resolved to their final values. The context is primarily the
        JobCollection within the jobs resides but also dependencies to other
        jobs and JobCollection's. Thus this JobCollection will apply its own
        configuration, like variables to add, tags to set, etc., to all its jobs
        and JobCollection's.

        Copies means what it says, that the returned job are not the same job
        objects, originally added to this JobCollection, but copies of them.

        Nested means, that also jobs from JobCollection's within this
        JobCollection, are returned, as well as jobs from JobCollection's within
        JobCollection's within this JobCollection and so on.
        '''
        return typing.cast(typing.List[Job], jsii.get(self, "populatedJobs"))

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List[ChildDict]:
        return typing.cast(typing.List[ChildDict], jsii.get(self, "children"))

    @children.setter
    def children(self, value: typing.List[ChildDict]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d884a03192750ebad3f4984fd76458601b4f922e83e0cde4ee82ea9e40d49b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "children", value)

    @builtins.property
    @jsii.member(jsii_name="orderedTags")
    def ordered_tags(self) -> OrderedStringSet:
        return typing.cast(OrderedStringSet, jsii.get(self, "orderedTags"))

    @ordered_tags.setter
    def ordered_tags(self, value: OrderedStringSet) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020fae99a60d2c4b4eacc7370ceafa3ae8de580635c43bbc3e7ad30885f7e304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderedTags", value)

    @builtins.property
    @jsii.member(jsii_name="orderedTagsForInitialization")
    def ordered_tags_for_initialization(self) -> OrderedStringSet:
        return typing.cast(OrderedStringSet, jsii.get(self, "orderedTagsForInitialization"))

    @ordered_tags_for_initialization.setter
    def ordered_tags_for_initialization(self, value: OrderedStringSet) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37ce8f87fc09777d997e039769aa954d40880baa7d68702811d01ea13f6ba31d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderedTagsForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="orderedTagsForReplacement")
    def ordered_tags_for_replacement(self) -> OrderedStringSet:
        return typing.cast(OrderedStringSet, jsii.get(self, "orderedTagsForReplacement"))

    @ordered_tags_for_replacement.setter
    def ordered_tags_for_replacement(self, value: OrderedStringSet) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ccb162d3b020c317be07cba3df0fe16a61ceeb9584d3016f969be36aef5e42a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderedTagsForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="parents")
    def parents(self) -> typing.List[typing.Union[Job, "JobCollection"]]:
        return typing.cast(typing.List[typing.Union[Job, "JobCollection"]], jsii.get(self, "parents"))

    @parents.setter
    def parents(self, value: typing.List[typing.Union[Job, "JobCollection"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00f70279d2b723bc21d160de5df77048749cb15e3c5d8bb007b3c102fa2f7e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parents", value)

    @builtins.property
    @jsii.member(jsii_name="allowFailureForInitialization")
    def allow_failure_for_initialization(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]]:
        return typing.cast(typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]], jsii.get(self, "allowFailureForInitialization"))

    @allow_failure_for_initialization.setter
    def allow_failure_for_initialization(
        self,
        value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8010f26a7f012891da851efeca7355e695a397fca0f7c558334a2823fc0b0f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailureForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="allowFailureForReplacement")
    def allow_failure_for_replacement(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]]:
        return typing.cast(typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]], jsii.get(self, "allowFailureForReplacement"))

    @allow_failure_for_replacement.setter
    def allow_failure_for_replacement(
        self,
        value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccb6d32a30dc48a62c971eda38f71296dc661f34966195dcadf95c534940dd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowFailureForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Optional["Artifacts"]:
        return typing.cast(typing.Optional["Artifacts"], jsii.get(self, "artifacts"))

    @artifacts.setter
    def artifacts(self, value: typing.Optional["Artifacts"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0150f47b890e3e8c0aaf17a71490642c1a0f57854515ab728e0a02be72f417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifacts", value)

    @builtins.property
    @jsii.member(jsii_name="artifactsForInitialization")
    def artifacts_for_initialization(self) -> typing.Optional["Artifacts"]:
        return typing.cast(typing.Optional["Artifacts"], jsii.get(self, "artifactsForInitialization"))

    @artifacts_for_initialization.setter
    def artifacts_for_initialization(self, value: typing.Optional["Artifacts"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3f56105f78adb7e1d8b7d339e09885a6f5da21efd5d662b12d1caf9cb9d71a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactsForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="artifactsForReplacement")
    def artifacts_for_replacement(self) -> typing.Optional["Artifacts"]:
        return typing.cast(typing.Optional["Artifacts"], jsii.get(self, "artifactsForReplacement"))

    @artifacts_for_replacement.setter
    def artifacts_for_replacement(self, value: typing.Optional["Artifacts"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11405e5ad5ee8410ffbcb19fe775c0e9de8028505462748df8772a21d4c7604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactsForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> typing.Optional[Cache]:
        return typing.cast(typing.Optional[Cache], jsii.get(self, "cache"))

    @cache.setter
    def cache(self, value: typing.Optional[Cache]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cfa065fa29d1dbffd8532c2b4796d8ec0ade220c8029a6a048b53395b0d9e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cache", value)

    @builtins.property
    @jsii.member(jsii_name="cacheForInitialization")
    def cache_for_initialization(self) -> typing.Optional[Cache]:
        return typing.cast(typing.Optional[Cache], jsii.get(self, "cacheForInitialization"))

    @cache_for_initialization.setter
    def cache_for_initialization(self, value: typing.Optional[Cache]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65bd39e1de9367c6b0bff5bad820b3d65b2e71df866ef37a484a0b76335fb160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(
        self,
    ) -> typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]], jsii.get(self, "dependencies"))

    @dependencies.setter
    def dependencies(
        self,
        value: typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee0a9759f2e776c42231317e7d2b7ee3264b893da4c0899cde07f7530631cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencies", value)

    @builtins.property
    @jsii.member(jsii_name="dependenciesForInitialization")
    def dependencies_for_initialization(
        self,
    ) -> typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]], jsii.get(self, "dependenciesForInitialization"))

    @dependencies_for_initialization.setter
    def dependencies_for_initialization(
        self,
        value: typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5dbc1f13d1b166b200af0d22405b54677a97d49e47c497ebeb9b3a54f8c6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependenciesForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="dependenciesForReplacement")
    def dependencies_for_replacement(
        self,
    ) -> typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]], jsii.get(self, "dependenciesForReplacement"))

    @dependencies_for_replacement.setter
    def dependencies_for_replacement(
        self,
        value: typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7665c71aaff63d6e2f8516550bf5b26b745d4af6223e82ecb5e80d090ca7dee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependenciesForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="imageForInitialization")
    def image_for_initialization(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, Image]]:
        return typing.cast(typing.Optional[typing.Union[builtins.str, Image]], jsii.get(self, "imageForInitialization"))

    @image_for_initialization.setter
    def image_for_initialization(
        self,
        value: typing.Optional[typing.Union[builtins.str, Image]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f864c2feadb144d2585bca7a06e0abacee84879e0047fc313b7a50cea59cccfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="imageForReplacement")
    def image_for_replacement(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, Image]]:
        return typing.cast(typing.Optional[typing.Union[builtins.str, Image]], jsii.get(self, "imageForReplacement"))

    @image_for_replacement.setter
    def image_for_replacement(
        self,
        value: typing.Optional[typing.Union[builtins.str, Image]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90dbe040df39787f521b4ca5c6ba4884183c92369cd61d11482ebc12c95df945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="needs")
    def needs(
        self,
    ) -> typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]], jsii.get(self, "needs"))

    @needs.setter
    def needs(
        self,
        value: typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad1158610f11daa642534c94ef06b19443edd5980c3e079e33efdbdab80f8c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "needs", value)

    @builtins.property
    @jsii.member(jsii_name="needsForInitialization")
    def needs_for_initialization(
        self,
    ) -> typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]], jsii.get(self, "needsForInitialization"))

    @needs_for_initialization.setter
    def needs_for_initialization(
        self,
        value: typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fefcc9950445b162f148c953f2160becbb8a75ebd8cd86baec8ec42592dea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "needsForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="needsForReplacement")
    def needs_for_replacement(
        self,
    ) -> typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]]:
        return typing.cast(typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]], jsii.get(self, "needsForReplacement"))

    @needs_for_replacement.setter
    def needs_for_replacement(
        self,
        value: typing.Optional[typing.List[typing.Union[Job, "JobCollection", Need]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa5cfeee37aa55014cd5ccc7c97fe8d067e69ff8c899926f1fc8607d5ae92b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "needsForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="rulesForInitialization")
    def rules_for_initialization(self) -> typing.Optional[typing.List[Rule]]:
        return typing.cast(typing.Optional[typing.List[Rule]], jsii.get(self, "rulesForInitialization"))

    @rules_for_initialization.setter
    def rules_for_initialization(
        self,
        value: typing.Optional[typing.List[Rule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba39e68be33dd8f847f289aec5d440ca3d90ed3e7fe32ec1a612004f0bf27a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="rulesForReplacement")
    def rules_for_replacement(self) -> typing.Optional[typing.List[Rule]]:
        return typing.cast(typing.Optional[typing.List[Rule]], jsii.get(self, "rulesForReplacement"))

    @rules_for_replacement.setter
    def rules_for_replacement(self, value: typing.Optional[typing.List[Rule]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9375709ac002147e2659f0d6ab412b8251e0ca73c9c8d1c7ecc67d9f4aa1c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesForReplacement", value)

    @builtins.property
    @jsii.member(jsii_name="rulesToAppend")
    def rules_to_append(self) -> typing.Optional[typing.List[Rule]]:
        return typing.cast(typing.Optional[typing.List[Rule]], jsii.get(self, "rulesToAppend"))

    @rules_to_append.setter
    def rules_to_append(self, value: typing.Optional[typing.List[Rule]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd94f3950086c7763e4abda6a3d63b1aaf08d517577753832645b6c3a8fb7ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesToAppend", value)

    @builtins.property
    @jsii.member(jsii_name="rulesToPrepend")
    def rules_to_prepend(self) -> typing.Optional[typing.List[Rule]]:
        return typing.cast(typing.Optional[typing.List[Rule]], jsii.get(self, "rulesToPrepend"))

    @rules_to_prepend.setter
    def rules_to_prepend(self, value: typing.Optional[typing.List[Rule]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144ba7ab97d18f915ade61bb9605b3bb0e29def0712ebfc8d96913dcfcbebc4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesToPrepend", value)

    @builtins.property
    @jsii.member(jsii_name="scriptsToAppend")
    def scripts_to_append(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scriptsToAppend"))

    @scripts_to_append.setter
    def scripts_to_append(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d28f2b8a3d9a36e640a646953a54af2370a1c433bc4d837bd61d70a253e4227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptsToAppend", value)

    @builtins.property
    @jsii.member(jsii_name="scriptsToPrepend")
    def scripts_to_prepend(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scriptsToPrepend"))

    @scripts_to_prepend.setter
    def scripts_to_prepend(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16fd5270e77a60218882f41670ddff30b54e85360e41cc7e9e1d0173c769fc07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptsToPrepend", value)

    @builtins.property
    @jsii.member(jsii_name="variables")
    def variables(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variables"))

    @variables.setter
    def variables(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bcba7ac6850a2cdf090f3b57395f3a262e6f4e3dc58d6a62c29de6977415737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variables", value)

    @builtins.property
    @jsii.member(jsii_name="variablesForInitialization")
    def variables_for_initialization(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variablesForInitialization"))

    @variables_for_initialization.setter
    def variables_for_initialization(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b57bc614191724c588f2273cd840e397d88423279b42dffa1f99ede098574a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variablesForInitialization", value)

    @builtins.property
    @jsii.member(jsii_name="variablesForReplacement")
    def variables_for_replacement(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "variablesForReplacement"))

    @variables_for_replacement.setter
    def variables_for_replacement(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5a961f3b0447cab3e54a44811515199806e94203ed2200dd734b1c63aba280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variablesForReplacement", value)


@jsii.implements(IPagesJob)
class PagesJob(Job, metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.PagesJob"):
    '''This is a special kind of jobs which deploys Gitlab Pages.

    This job has the static name ``pages`` and the static artifacts path
    ``./public``. Both preconfigurations can't be altered and are required for
    deploying Gitlab Pages properly. All methods which would typically alter the
    name, stage and artifacts of a job are overwritten with an empty
    implementation.

    This job is only for deploying Gitlab Pages artifacts within the ``./public``
    artifacts path. To create the artifacts you have to run jobs, that generate
    those artifacts within the same ``./public`` artifacts path, before this
    PagesJob in the pipeline.

    Because the name of the job can't be altered, this job may only exist once
    in the generated pipeline output.
    Typically you should add the PagesJob to the ``gcix.Pipeline``.

    The PagesJob is also preconfigured with the stage ``pages`` and the image
    ``alpine:latest``. To change the stage of this job, use the ``assignStage()``
    method. Please mention to run this job in a stage after all jobs, that fill
    the ``public`` artifacts path with content.

    Here a simple example how to use the GitlabPages job::

       const pipeline = new Pipeline()
       pipeline.addChildren({
           new Job({stage: "deploy", scripts: ["./create-html.sh"]).assingArtifacts(new Artifacts({paths: ["public"]})}),
           new PagesJob(),
       })
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="assignStage")
    def assign_stage(self, stage: builtins.str) -> "PagesJob":
        '''Set the name of this jobs stage to a value other than ``pages``.

        :param stage: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf71ab3136953b215374020d76f0cc0822594d4e74dc1d4bd715ef1e286d5544)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast("PagesJob", jsii.invoke(self, "assignStage", [stage]))

    @jsii.member(jsii_name="copy")
    def copy(self) -> Job:
        '''Returns an independent, deep copy object of this job.'''
        return typing.cast(Job, jsii.invoke(self, "copy", []))

    @jsii.member(jsii_name="extendName")
    def extend_name(self, name: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs name.

        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6577d3e2c3ea74e23ec845aaf1ef98de7efaa52a11c10ee3668025ddd828750)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "extendName", [name]))

    @jsii.member(jsii_name="extendStage")
    def extend_stage(self, name: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs name and stage.

        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601ddea37bfd612cfd256ac4bbed07e02cfcc3f2b82532c9f110eee789c068d3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "extendStage", [name]))

    @jsii.member(jsii_name="extendStageValue")
    def extend_stage_value(self, name: builtins.str) -> None:
        '''This method is used by ``gcix.JobCollection``s to populate the jobs stage.

        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db7b15403a371f7c56c4455186a03d6739aaa4ea519f9d8f10acb8ea445c187)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(None, jsii.invoke(self, "extendStageValue", [name]))

    @jsii.member(jsii_name="getAllInstanceNames")
    def get_all_instance_names(
        self,
        child: typing.Optional[typing.Union[Job, JobCollection]] = None,
    ) -> OrderedStringSet:
        '''Return all instance names from the given child.

        That means all combinations of the childs name and stage within this
        sequence and all parent sequences.

        :param child: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac9f6009e6ceaeb01744958063b9239cf9418bcf6ce43d4f6742d476c7046199)
            check_type(argname="argument child", value=child, expected_type=type_hints["child"])
        return typing.cast(OrderedStringSet, jsii.invoke(self, "getAllInstanceNames", [child]))


@jsii.implements(IPipeline)
class Pipeline(JobCollection, metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.Pipeline"):
    def __init__(
        self,
        *,
        includes: typing.Optional[typing.Sequence[Include]] = None,
    ) -> None:
        '''A Pipeline is the uppermost container of ``gcix.Job``s and ``gcix.JobCollection``s.

        A Pipeline is a ``gcix.JobCollection`` itself but has the additional method ``Pipeline.write_yaml()``.
        This method is responsible for writing the whole Gitlab CI pipeline to a YAML file which could then feed
        the dynamic child pipeline.

        :param includes: You can add global ``gcix.Include``s to the pipeline. `Gitlab CI Documentation <https://docs.gitlab.com/ee/ci/yaml/#include>`_: *"Use include to include external YAML files in your CI/CD configuration."*.
        '''
        props = PipelineProps(includes=includes)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addChildren")
    def add_children(
        self,
        *,
        jobs_or_job_collections: typing.Sequence[typing.Union[Job, JobCollection]],
        name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> JobCollection:
        '''Add ``gcix.Job``s or other ``gcix.JobCollection``s to this JobCollection.

        Adding a child creates a copy of that child. You should provide a name or
        stage when adding children, to make them different from other places
        where they will be used.

        :param jobs_or_job_collections: 
        :param name: 
        :param stage: 
        '''
        props = AddChildrenProps(
            jobs_or_job_collections=jobs_or_job_collections, name=name, stage=stage
        )

        return typing.cast(JobCollection, jsii.invoke(self, "addChildren", [props]))

    @jsii.member(jsii_name="addInclude")
    def add_include(self, include: Include) -> "Pipeline":
        '''Let you add global ``gcix.Include``s to the pipeline. `Gitlab CI Documentation <https://docs.gitlab.com/ee/ci/yaml/#include>`_: *"Use include to include external YAML files in your CI/CD configuration."*.

        :param include: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22bb21f984d9a957ce4cd6249b1d3eda009f9fad8470f2a2ed3e33c79818ad5d)
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        return typing.cast("Pipeline", jsii.invoke(self, "addInclude", [include]))

    @jsii.member(jsii_name="addServices")
    def add_services(self, services: typing.Sequence[Service]) -> "Pipeline":
        '''Add one or more ``gcix.Service``s to the pipeline.

        Gitlab CI Documentation: *"The services keyword defines a Docker image
        that runs during a job linked to the Docker image that the image keyword
        defines."*

        :param services: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518219648f52555f1dd663bc1a6d9611e3f2f1791f742920c6a0e72ef4293bdc)
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
        return typing.cast("Pipeline", jsii.invoke(self, "addServices", [services]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @jsii.member(jsii_name="writeYaml")
    def write_yaml(self, filename: typing.Optional[builtins.str] = None) -> None:
        '''Create the Gitlab CI YAML file from this pipeline object.

        Use that YAML file to trigger a child pipeline.

        :param filename: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe54c848f938b42878b9e4477e1de81ba9a0eba48c10316fc36700b4194ceb81)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        return typing.cast(None, jsii.invoke(self, "writeYaml", [filename]))

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(self) -> typing.List[Include]:
        return typing.cast(typing.List[Include], jsii.get(self, "includes"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> typing.List[Service]:
        return typing.cast(typing.List[Service], jsii.get(self, "service"))


@jsii.implements(ITriggerJob)
class TriggerJob(Job, metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.TriggerJob"):
    '''This class represents the `trigger <https://docs.gitlab.com/ee/ci/yaml/README.html#trigger>`_ job.

    Jobs with trigger can only use a
    `limited set of keywords <https://docs.gitlab.com/ee/ci/multi_project_pipelines.html#limitations>`_.
    For example, you can’t run commands with ``script``.

    Simple example::

       const triggerJob = new TriggerJob({
           stage: "trigger-other-job",
           project: "myteam/other-project",
           branch: "main",
           strategy: "depend",
       })
       triggerJob.appendRules(rules.onTags().never(), rules.onMain())

    :throws:

    Error when the limit of three child pipelines is exceeded.
    See https://docs.gitlab.com/ee/ci/parent_child_pipelines.html
    for more information.
    '''

    def __init__(
        self,
        *,
        branch: typing.Optional[builtins.str] = None,
        includes: typing.Optional[typing.Sequence[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: 
        :param includes: 
        :param name: 
        :param project: 
        :param stage: 
        :param strategy: 
        '''
        props = TriggerJobProps(
            branch=branch,
            includes=includes,
            name=name,
            project=project,
            stage=stage,
            strategy=strategy,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> typing.Optional[builtins.str]:
        '''The branch of ``project`` the pipeline should be triggered of.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cbc35e57a5d84ce369bf2bdff03574154554ecb8d1de2885fe78aceeb8a8b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value)

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(
        self,
    ) -> typing.Optional[typing.List[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]]:
        '''Include a pipeline to trigger (Parent-child pipeline trigger) Mutually exclusiv with ``project``.'''
        return typing.cast(typing.Optional[typing.List[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]], jsii.get(self, "includes"))

    @includes.setter
    def includes(
        self,
        value: typing.Optional[typing.List[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4229a956f31df104311d10b187f68bc911b250ae98306d3a832cc2ccb84f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includes", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> typing.Optional[builtins.str]:
        '''The full name of another Gitlab project to trigger (multi-project pipeline trigger).

        Mutually exclusive with ``includes``.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "project"))

    @project.setter
    def project(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e7740e40b673acd58127f23f30a706ffe63e24bfdc90bb4a904118fbcce5bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def strategy(self) -> typing.Optional[builtins.str]:
        '''Determines if the result of this pipeline depends on the triggered downstream pipeline (use ``TriggerStrategy.DEPEND``) or if just "fire and forget" the downstream pipeline (use ``None``).'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "strategy"))

    @strategy.setter
    def strategy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0091ce60c1e4494fd202a87f3c771bed351a6d42d9ffc8115b264ec45a598db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strategy", value)


@jsii.implements(IArtifacts)
class Artifacts(metaclass=jsii.JSIIMeta, jsii_type="@gcix/gcix.Artifacts"):
    '''This class represents the `artifacts <https://docs.gitlab.com/ee/ci/yaml/#artifacts>`_ keyword.

    Gitlab CI documentation: *"Use artifacts to specify a list of files and
    directories that are attached to the ``gcix.Job`` when it succeeds,
    fails, or always. [...] by default, ``gcix.Job``s in later stages
    automatically download all the artifacts created by jobs in earlier stages.
    You can control artifact download behavior in Job's with dependencies."*

    :raises: Error if when is not ``on_success``, ``on_failure`` or ``always``.
    '''

    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        expire_in: typing.Optional[builtins.str] = None,
        expose_as: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        public: typing.Optional[builtins.bool] = None,
        reports: typing.Optional[typing.Sequence[typing.Union[ArtifactsReport, typing.Dict[builtins.str, typing.Any]]]] = None,
        untracked: typing.Optional[builtins.bool] = None,
        when: typing.Optional[WhenStatement] = None,
    ) -> None:
        '''
        :param excludes: Paths that prevent files from being added to an artifacts archive.
        :param expire_in: How long the artifacts will be saved before it gets deleted.
        :param expose_as: Used to expose artifacts in merge requests.
        :param name: Name of the artifacts archive. Internally defaults to {PredefinedVariables.ciJobName}-{PredefinedVariables.ciCommitRefSlug}.
        :param paths: Paths relative to project directory ``$CI_PROJECT_DIR``, found files will be used to create the artifacts.
        :param public: True makes artifacts public.
        :param reports: Reports must be a valid dictionary, the key represents a ArtifactsReport and the value must be a valid relativ file path to the reports file.
        :param untracked: If true adds all untracked file to artifacts archive.
        :param when: When to upload artifacts, Only ``on_success``, ``on_failure`` or ``always`` is allowed.
        '''
        props = ArtifactsProps(
            excludes=excludes,
            expire_in=expire_in,
            expose_as=expose_as,
            name=name,
            paths=paths,
            public=public,
            reports=reports,
            untracked=untracked,
            when=when,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addExcludes")
    def add_excludes(self, excludes: typing.Sequence[builtins.str]) -> None:
        '''
        :param excludes: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc49353e37d8ad2a0610c6c0b08ce860e0d9b2b9a70ed069768a7483eb608e2)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
        return typing.cast(None, jsii.invoke(self, "addExcludes", [excludes]))

    @jsii.member(jsii_name="addPaths")
    def add_paths(self, paths: typing.Sequence[builtins.str]) -> None:
        '''
        :param paths: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8b4a0edc18e1f688fc2760748dcd456d3534acbf1948a7a776e4f08ee84925)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        return typing.cast(None, jsii.invoke(self, "addPaths", [paths]))

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, comparable: IBase) -> builtins.bool:
        '''``isEqual`` checks if ``this`` object is equal to given object.

        :param comparable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ea9a02de52d1dd351ddd32831cbc225a4799d162305f9f438fe675fe46c3b5)
            check_type(argname="argument comparable", value=comparable, expected_type=type_hints["comparable"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEqual", [comparable]))

    @jsii.member(jsii_name="render")
    def render(self) -> typing.Any:
        '''Returns a representation of any object which implements ``IBase``.

        The rendered representation is used by the ``gcix`` to dump it
        in YAML format as part of the ``.gitlab-ci.yml`` pipeline.

        :return: RenderdArtifacts
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @builtins.property
    @jsii.member(jsii_name="expireIn")
    def expire_in(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expireIn"))

    @builtins.property
    @jsii.member(jsii_name="exposeAs")
    def expose_as(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exposeAs"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="public")
    def public(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "public"))

    @builtins.property
    @jsii.member(jsii_name="reports")
    def reports(self) -> typing.Optional[typing.List[ArtifactsReport]]:
        return typing.cast(typing.Optional[typing.List[ArtifactsReport]], jsii.get(self, "reports"))

    @builtins.property
    @jsii.member(jsii_name="untracked")
    def untracked(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "untracked"))

    @builtins.property
    @jsii.member(jsii_name="when")
    def when(self) -> typing.Optional[WhenStatement]:
        return typing.cast(typing.Optional[WhenStatement], jsii.get(self, "when"))

    @builtins.property
    @jsii.member(jsii_name="orderedExcludes")
    def ordered_excludes(self) -> OrderedStringSet:
        return typing.cast(OrderedStringSet, jsii.get(self, "orderedExcludes"))

    @ordered_excludes.setter
    def ordered_excludes(self, value: OrderedStringSet) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b3ef4ee3502465f1fa2c9802f8541985f1e48407552ea6909dfc2b79c9512c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderedExcludes", value)

    @builtins.property
    @jsii.member(jsii_name="orderedPaths")
    def ordered_paths(self) -> OrderedStringSet:
        return typing.cast(OrderedStringSet, jsii.get(self, "orderedPaths"))

    @ordered_paths.setter
    def ordered_paths(self, value: OrderedStringSet) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539fa9abb7f73b7fa20b02adeaeff1784fadc1c06f4f9342be06de91d7f9a313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderedPaths", value)


__all__ = [
    "AddChildrenProps",
    "Artifacts",
    "ArtifactsProps",
    "ArtifactsReport",
    "Cache",
    "CacheKey",
    "CacheKeyProps",
    "CachePolicy",
    "CacheProps",
    "ChildDict",
    "IArtifacts",
    "IBase",
    "ICache",
    "ICacheKey",
    "IImage",
    "IInclude",
    "IIncludeArtifact",
    "IIncludeFile",
    "IIncludeLocal",
    "IIncludeRemote",
    "IIncludeTemplate",
    "IJob",
    "IJobBase",
    "IJobCollection",
    "IJobCollectionBase",
    "INeed",
    "IPagesJob",
    "IPipeline",
    "IRule",
    "IService",
    "ITriggerJob",
    "Image",
    "ImageProps",
    "Include",
    "IncludeArtifact",
    "IncludeArtifactProps",
    "IncludeFile",
    "IncludeFileProps",
    "IncludeLocal",
    "IncludeLocalProps",
    "IncludeRemote",
    "IncludeRemoteProps",
    "IncludeTemplate",
    "IncludeTemplateProps",
    "Job",
    "JobCollection",
    "JobProps",
    "Need",
    "NeedProps",
    "OrderedStringSet",
    "PagesJob",
    "Pipeline",
    "PipelineProps",
    "PredefinedVariables",
    "RenderedImage",
    "RenderedIncludeArtifact",
    "RenderedIncludeFile",
    "RenderedIncludeLocal",
    "RenderedIncludeRemote",
    "RenderedIncludeTemplate",
    "RenderedJob",
    "Rule",
    "RuleLib",
    "RuleProps",
    "Service",
    "ServiceProps",
    "TriggerJob",
    "TriggerJobProps",
    "WhenStatement",
    "aws",
    "container",
    "git",
    "gitlab",
    "linux",
    "python",
    "security",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import aws
from . import container
from . import git
from . import gitlab
from . import linux
from . import python
from . import security

def _typecheckingstub__df60c334bb3349c666a96c0b9eb0a0fd10bedfe170f49913f799b055d493ec1f(
    *,
    jobs_or_job_collections: typing.Sequence[typing.Union[Job, JobCollection]],
    name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f626d293a27ed91c78507cb1db1ee62396670f50e62b9f2c7edaa3b96329be1a(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    expire_in: typing.Optional[builtins.str] = None,
    expose_as: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    public: typing.Optional[builtins.bool] = None,
    reports: typing.Optional[typing.Sequence[typing.Union[ArtifactsReport, typing.Dict[builtins.str, typing.Any]]]] = None,
    untracked: typing.Optional[builtins.bool] = None,
    when: typing.Optional[WhenStatement] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50db0ecd289671e1aea241660ca1fde603d026802a5373182b4954af283cec7(
    *,
    file: builtins.str,
    report_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55fe4c35d97b905706af6ab04c98d2856dcbde83ceb7f14ee2dee01194eb6327(
    *,
    files: typing.Optional[typing.Sequence[builtins.str]] = None,
    key: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a2924781897361b6f1944ca54c776e0cb84ef97befcf405999f1f3e24fe342(
    *,
    paths: typing.Sequence[builtins.str],
    cache_key: typing.Optional[CacheKey] = None,
    policy: typing.Optional[CachePolicy] = None,
    untracked: typing.Optional[builtins.bool] = None,
    when: typing.Optional[WhenStatement] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ffe8a304fc91b334af5c8ae0a40aa88351b253967dd52f61e50e8f5087b24d(
    *,
    child: typing.Union[Job, JobCollection],
    name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b802032a1c461219b94468e0001211e7fa3a98362391007c612b7f50f5be09(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2a2d3292a09166e2c85abc407e33a4b0b0c26e2917700c4f680d577479fc92(
    entrypoint: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb5145e81595053717d524ea935386d483337ec4a56c299aeba9198aa1319f8(
    tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8aee6bf51572eeeb275012082671627b86e9490f1dbb1db4c5cb84dd8fa4e52(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e628bdb293dd53db6a2f0816a2ac17bfbee5d4b02ba83bd93fdd6f485e494bc(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11c85b5c3830a93f7673707ad357ec8ff0dde3d65439976c2bfb5acaef9d0f2(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac8f9a4d174a64d5c16c0fe9e19e0e2c7db098410e99d21fc33ad34bd7c324f(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75844a5c81111f43121da92b1093077b892bc159153efe9908f73f142b4d604(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f5eeeadc0839ee43fe0900370bda5f6b4d589d8f41959d43c55488525e340e(
    scripts: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5f0d4ca99667d89a42ee6c3e5fe148cebda32c2d4ede5ce959b9c23be250c4(
    artifacts: Artifacts,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b03c43eafa4deb9248e78940883defec43d04a5628eead3c6c2774d4e504cf7(
    cache: Cache,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b1d8712cbbdf0e62e8e7b59ad3dd795707957652047f1c88a2a80afa273e2f(
    child: typing.Optional[typing.Union[Job, JobCollection]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd0bb7b0e3d0dcbe8ccf63092df6ac928317aeef53b3ef82004df5eb92b4ad8(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2ea334fb58d11a07160912556aac724a6f68bfdc320ee0ba009bccc6e73a6a(
    scripts: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ed935f54f176dfdc4965e1d7085adc5f78d1a96f54b80cd0099a35eebe2fd6(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9630d892d6f3d4bf0dc8151cf297d433db5836784629f91b76e002d4cefe93e(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72eae7b63d66111c68fbdb60f5e300b6e5d13d2e320a9966dc44633911ba244(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460fd04af2f8d7f9bcdc8eed0a359faf483a92b0d620f98ed09b0d166da5667a(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed35c4a51a06708dab9a9e45d1872c1b8093d8e5048d76d15ddd9d8b989f6e1(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6038da2730c42a2edc87e557f36891028cbd10a4a550eec08abcb16050773e01(
    scripts: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9811da6c6dc7d5c5fb64242904876c23949d64052c73add9321c01dd27d3fa69(
    artifacts: Artifacts,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509908ec5f25755b6cff8829d915602bdc20f223d63af18b0bccc725d86eac53(
    cache: Cache,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038e7a4899cf6f020080b690e52525857fa7ee8957a8f91439fe84c60abe678e(
    child: typing.Optional[typing.Union[Job, JobCollection]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7e723df0002afa54736fd55b3faa1a343289181dabae9f5cbc5020608cb200(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62dc3a436bac4c95e74e3e70dd16aac82e0750b4966b1da2303aefc39fbb8082(
    scripts: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9188c1787279eb95b2345d9ee3cf9eecc815fdea5f6a96b76b96212a604c4978(
    stage: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9062d2c93cff55583c61a62346b43157576f6dd57b8f0d4ee4c8855522f6426d(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1fa047341648a1112b54541286025899a02708f3b36c4bee831091c4b8986d(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14db9a17126777706c353f7a3903e56d747ff5ca3938a0b80e5ae592c34ef584(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e28fe324efc138161bf4679a2d82b5a90737d2bf5d09571a7ae4814a77b990(
    include: Include,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b779b1ab3d54999ef8df97b55356d16db35549e20c989908d936a6e334e27b(
    services: typing.Sequence[Service],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96c454ab0a3f58392b05e7d80dc3a7df875c37d61c317481c85f54e9bb5f1d7(
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7eb42bf680cbe707b884181d461186d13f501dc27feb2ba28b81c356c041b3(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df4d15435ffe1434f16f5a77ca3067eb6d1e89660e177ea313c1544ea86d39d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f688d53e106b53582f0d712821dac997079d1479f6bf480ffdfdad656dad406(
    value: typing.Optional[typing.List[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade450b81a48ddc3723f73a18409fa603a8144bd2f94a5803fa1a4f8e103cf8e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bdf94dfa91262761d1f8e26436a7f93e4e7c281ce993a5314e8719c31f4743(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2a35ee4709de564436ef9700b1deb2e1db70796e4d2420b43443a1863bc095(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e5ec7913b580d4210605bbccf430e902713f76606c23b2dfc862e2567edac2(
    entrypoint: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2dcff1af5d25512515e4467781177e01397539668630064709b27590be91f0f(
    tag: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f239025515d1dc0e5da1f102c2744bb938dceae0d3e0c4ebe1ff277ce65f352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2046cb85c036453c62ad247747305bd0672c03185a4794cffe555bfed6590490(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fbdfd006a3101ae02bf08db6032fc7decf3d83dcbe48a1c070dcd32d2b4ab8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a206b1d7a64271bf19bfa8eec764c2d1ced5779801630b5916ef78d8aca78ec3(
    *,
    name: builtins.str,
    entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34cb8f048535f4cf504557cc2b72021e05a1225d61437bcd7eacab367a3a74b9(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6638cd4c88920fbc055b25b74a83ede6f3f7a1be640dfecacc2ed9655b30be7b(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe231effbeb59a4e5b310a4bd72c6777c20816c2fae07527972344979aeda40(
    *,
    artifact: builtins.str,
    job: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d092556027df5bc534b1b982f559c3a4239787d8fa1946366627c13d0ab8c0(
    *,
    file: builtins.str,
    project: builtins.str,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3dcbd3670d94ab59398ee3faaaa53839dece0252157a37879dff6ef28e1fad4(
    *,
    local: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2928dfd23c62e7a2ed12b3f1f4943bd6ac588e797b2f6bff3e4f2cb665cf4bba(
    *,
    remote: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4efed7ce19a60907db78b31497f8feee1fd1f69e18be3c2e46916185d5d36c(
    *,
    template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cbed1928941b7d9ab02facad79a3cc0b1c10eac94f6ea0777578cc97ae2c4a(
    *,
    scripts: typing.Sequence[builtins.str],
    allow_failure: typing.Optional[typing.Union[builtins.bool, typing.Sequence[jsii.Number]]] = None,
    artifacts: typing.Optional[Artifacts] = None,
    cache: typing.Optional[Cache] = None,
    dependencies: typing.Optional[typing.Sequence[typing.Union[Job, JobCollection]]] = None,
    image: typing.Optional[typing.Union[builtins.str, Image]] = None,
    name: typing.Optional[builtins.str] = None,
    needs: typing.Optional[typing.Sequence[typing.Union[Job, JobCollection, Need]]] = None,
    rules: typing.Optional[typing.Sequence[Rule]] = None,
    stage: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee4b3bd273a1b5cb9a8321ea15f051d48d43d483253502450bbeab70c098bd5(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d198d6a7a7b04f4ad8b480ac29f9e68d6bcb4e0de77626ebfda46cfd7b7cea(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50f041f3ef47b596e0b2ce31821eb03d2ed75d5929d6a8bf5da9238de546e42(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb0a517c21b40a0ad6c3d47dd8207f97524ef628c60a068dbebbde7307bb52a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13713b719c82daa59c3d732be80bf8e00673ab95b0db7d29fa3fd8cc74ab6a06(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7e33fc9c788da70e893a43de03c4d4b38c8a62eb1b2b0aed9121326d435a00(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28141c95e97f81e6678f904f2b84cd83cc3a7cbde2b1a0cff6fca30c4da6df7(
    *,
    artifacts: typing.Optional[builtins.bool] = None,
    job: typing.Optional[builtins.str] = None,
    pipeline: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0e3c2a8d12e3bceb2cac68d625620e2accb5164e2849c102e70b3d23090106(
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faeabbcd55ceb46f5b615060a98ee7af2b34f0d181d10d30a069dbae8c7e6462(
    value: typing.Union[builtins.str, typing.Sequence[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f552f03d9ea9c8fa459a2bdec922969c01935e5028a816b687b00a57d5c93f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96a69145aaef180c6ed4c8a576da17c3ab04002311f011d5268c0dfc4ba918c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3477f8a77546ea9831987070462144f4c75f5f2d077cd7472f82ca430d8f9b42(
    *,
    includes: typing.Optional[typing.Sequence[Include]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62130a6aedd9621ef44fbfbd39f522f363028ee02b9197019c7ef95347186b45(
    *,
    name: builtins.str,
    entrypoint: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaec6b0c2f5b9bc0a3b9ba0d4306036a9874070bd74d94baf8eb41cb0e0d01ba(
    *,
    artifact: builtins.str,
    job: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e290ea0424ed1cf5a990f17ec7c453ad9292c275effb7a29d65ce8d13546fed5(
    *,
    file: builtins.str,
    project: builtins.str,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb630516648dea763828c2937fd40f93a61f3780f9034b0f797637733fcce359(
    *,
    local: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767f6aeebc514bdd0379b807bd7e8f1439350f3f143031e04168d9b6054cc8b6(
    *,
    remote: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643d1588e9d2e97427d55878c322abc5efae9e1fe124db975f524a7d9aca0613(
    *,
    template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dada20c2e64f84ae5060483b9b519132f4a6f47602899f297ee58bbfe0851d0(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7b865315adc72624c1abac74f9baa2656c915682f30f394e525f01389e9e5b(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e95b6f4a18d08cc8e3002a85450b2840df6eb98bd3fa63a82a70bef3b8f0cdc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe70022e9cc65c6beebd39215d6178cb4cceef6e8d05f8031aed0b2807215d9d(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e69f846467e29c36ad300c3fe972f7bbb8526d62c4dc20207b7649e68b37239(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7010546164a533f917900ba07195dd9d0e42527a106aad1ea5041884ec33bf48(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0dbb3e348c8c2582f4c3d2c0c0917223d347c97f3b53680906c3148b8ddec5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081adca324252fb94113a3c885f81b46fd8c1512eaa37200e22e7e17a416baaf(
    value: typing.Optional[WhenStatement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883b6a68a81893d6c9ded08f6240471fb8ebaf9608da477eda62eced7c143d0b(
    branch_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d49c4831cdafc79824344b9e38c01b0a4c349904e595164e602e76d9038236a(
    branch_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17680b9412fcc8a61ed4dd9ab67d6f960ee608993fab721fe7cd21eae45fbe1d(
    *,
    allow_failure: typing.Optional[builtins.bool] = None,
    changes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exists: typing.Optional[typing.Sequence[builtins.str]] = None,
    if_statement: typing.Optional[builtins.str] = None,
    variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    when: typing.Optional[WhenStatement] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36137733761a8c4aed62db7162c6232d0355ca060632e46c88c978da9197a6d6(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdd539c170dac097bec6b0c36f2d9cbb28b7272f0addd02ee7f5a57e13c8bf7(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a9bec0136da3d138ee5524a6e20dc4924dce668845b921e31d0fbc1f1a6d31(
    *,
    branch: typing.Optional[builtins.str] = None,
    includes: typing.Optional[typing.Sequence[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0183fdae5917a8cf383d235801473da1787225eaa02ab9ccff24a1bef7cc8738(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86e4fdcf9090775a868778e504b137a9c582c41ee934974f4f778cae6c6d5a5(
    value: CacheKey,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ae9ebf898d16c4f90435ef91068c2c0129887233421de38891ea963a586517(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b191468d86faae5a5ae68371c5ececb432d5a7b3e2432f08597a988c82123113(
    value: typing.Optional[CachePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9981b23dea0fefe2c794065c6a2610d50177a89dc0d081cfb5510c0e0ba4b8(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5413ae83fada192ab46461a6b711b3e34dd05fcf981f785326131006a4d7ba73(
    value: typing.Optional[WhenStatement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31e0b17fe36d665eeeef4e7aedceef00c8cb9509deaa146ca235892d42339ed(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a0620d883946f34a3867e71556506f18a2b690d9be847becc7d127f1bb243c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b14df8ab7205cb996776eacabc1a3c8e2a1f108f573daf0164a92c74bb262b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94e85a980c5516fee35ca39218361f799e4876b39b2c3ac9c8ce8dba86c1951(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b5b8c4ba7633202752f68da52f6ea66904445bf79b755180cf48d82eff0b7f2(
    excludes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7614a51c2e49545a8ed8d70ff4ed30c7fe5673edaaf959336145530398444f2(
    paths: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf96137fbb57c57d1030d349ff02fbd74594d2f66b12e7d4c0bb4f274d4cfc6(
    value: typing.Optional[Job],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a134b11e1ad65606a69cc0c5e4d9d932441690495879985927dbb1db87638088(
    parent: typing.Union[Job, JobCollection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a9854a6cdb23124efa141c8b9b00ba0ef2bf8250867ae138d16604d0b51e4f(
    allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7730f2ccc4b8c9213f50f0e50d1c46902750aa724adf2c4e23378dd11e5be925(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbcdcaec0006e696ba00afc16746dda9ba125b27ceb67584a6c7196c6f9e9cc(
    image: typing.Union[builtins.str, Image],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46bcc7245d8c2b9e48b79b3c95ef4f945046523a8c28f0da061549043a6fdab7(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad29f55eaaabf289c63253da4efa91842cb25be90c6877f1ddc74036ce79ac1(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f664bbcc750184adaa32f039a01fe87ccabef41cf30faa1e91995d0beaa112a(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2f2b757cb76f3fa887f7a5caffd94fe9a339333d431666c4c7905f3488177d(
    stage: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37512d3f1c106d4b00d4ea2427bdc75dac56aa97bad4983020ac437339ee9b4(
    stage: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce374c03318c12e49c9ccafdbc958569117f5dc171d0594c3551439750e0983(
    value: typing.List[ChildDict],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bbb7310bbdbd6426286205b78849eadb3f2fddf66c55ff578788f0d8799f9d2(
    value: OrderedStringSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb114e52af4b58ffa72c76d15d44a685595ea11b02da3bb6b732e4728fc0fe2(
    value: OrderedStringSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924fa58aa9f55459d00fa413efc595d87b8d63bb2dbac214b1529f96285d2b16(
    value: OrderedStringSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87380f08cd21392b245906f52afd056bb7bfc2b2df9b1c53ac84ba401d0cde1e(
    value: typing.List[typing.Union[Job, JobCollection]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4713420b5120162bd4c3efb9eb6a96e7b26cd0de808a786f3aa7a6ed7829f739(
    value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d16c8e870a92ac208345b5ac5b9e57305f5f2b332da630c3adf973b22a8631(
    value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800e6fd839dba4dc782d83b6fe96b46aac96ca4ae90386bdc94fc2cb5fee4d09(
    value: typing.Optional[Artifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5814f2b08c7a25d56ef31ed50b4a62a958b9acb5c65f827ca4745b5bacba1d04(
    value: typing.Optional[Artifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1927e02979834ceb11c4218027e92f100e3a4ba08370df25772ced608cbb3fb3(
    value: typing.Optional[Artifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165518ad606b6deaa654cafa77c1948747a3eeaa82478113ccbd5a371456d44b(
    value: typing.Optional[Cache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4e060d038f6c70721ff5d4f44f7291da06b2e1a27c855479635c78c2e36bac(
    value: typing.Optional[Cache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d29466e344000e02a13dfa43165f522a87dc3cc60bf38de9c200c73fbda61b(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f35524c5b155c2bf7ba26231196e402225fbc2cbcc5e4e4edb6f645429e5ee3(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d67c8b1a9eda875c58e35e7cf2c724d2cb1ec6a34adf52d194fb242ece22c8(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437f18fccd4e9fbbc5dd6edfc97e247a393ec912b32b1e962024c7ec2a819f13(
    value: typing.Optional[typing.Union[builtins.str, Image]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed07e70cbdd86434500eac7b3844d882ec5dc29e83d145a7bad125a09836698(
    value: typing.Optional[typing.Union[builtins.str, Image]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3924c92afb045dc0f499a2c3f57bd234c45e6e35cce5bdaa5dc9a11b0d60c9de(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463f7c8632c746a867ae8963f6b7ecfce290f49308e20c117299f9f0b6435525(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4c15a84c91915d015a98a495f261fe0bc292fd9556f2e2828541a4db83822a(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b28a39469fca1a505c49931b555665f211be55c751f2f5f15042e6640a7c465(
    value: typing.Optional[typing.List[Rule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4f3c166a56a27f71302cc0e190965e0c21bc65aa0bdd2ec25087e139dfe5e7(
    value: typing.Optional[typing.List[Rule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f96572ea161c18f87c8389bbb82399236232bab6cd5bbf6abebde4ed1ea2ff6(
    value: typing.Optional[typing.List[Rule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cccb9df8e4dec5431a67a3efb3c5b68359970e910c8b4848395078ca1ee8cf(
    value: typing.Optional[typing.List[Rule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e5b1c45f75b4231f79550e1a3aa2a451598f07f90dc5c1370b112d6bb30bec(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7ce1bc9adfe77dce0846ffd4bfbb42c00c6a5461cef05959a206ab95e2cc95(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ba53eb89a1220b77e8d246920f5d1d493e011367d63af1c3f59cbd5a54dc0b(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba70304a311fbb2a0bce9781b2b335896e010b7f432d113d52137d6f5e5c670(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620af3bad665631d9118208b10f6e2c10f078d1dd147228dadcdbe679ecc8025(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03777d712d99eca1625438ac0f95a7fe10768d5338c879c44c7398ac9f6ea504(
    parent: JobCollection,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5387c850358faf7f706c15e46d31610050877fb3d21e61e87ab9e1b37d342a71(
    allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a97e83dc7ff8a14d0c568ac16545b1bb57a722286a5426e5ad67a752d5214b(
    artifacts: Artifacts,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0181c42295494c9b48c2e4c414b843abb6fb34e9517474823787ce2525a1781(
    cache: Cache,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9aa08b460359399ef73f771713288180f56d37fa2fc473735b6e3062eddff2b(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9cb4619acadea11cc54e7e8e11e287580fd542190c2311ecbe6297088069c5(
    image: typing.Union[builtins.str, Image],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2cb512fd29fb38c1fd29b00d52a5029ecab4e4fc0060c1a73eda98718e3099(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503b25afaad5b3a95023281da352be04b22dc753f0badcc3a707591d9ab35ab5(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58148eded3196a8d1778f4f7a689f88b4ac1698f0b59f294e1fa028c54d6acc5(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e713143f5860e1bbebec8cf9f48b9faade58bdf769d329049fd1c7c17f528cf(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de206756d2c823c2bcfef0d2825f3b535dcff8fc0456e0ba7ced9d307bfd9d4(
    allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b867e206d8134a599be691d8340c9613ecfd2eeec79c732f2458dc5af93625(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2894761e19594ae15c6d28747a74a7790e903da192f64884c854acea95d180(
    image: typing.Union[builtins.str, Image],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab56faa06054c66095bbea7ce370e78145d0d1b9b759c05d48d75b21579510dd(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec78f97b536b9bd1e9abe68d46985468f4c1b546ea63925c5b54d7d29758c087(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b300cdc454d508866352523585ce60b65f470797886b0fd1265c71a53c53a8a9(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9b96730d3dc815593bd4221cda8585e45d579a28c3537bf882917ad3457b84(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a48c4d96775cb493b2af94f11cdc8d7ceb50c61ab3b14ad8854081299da1bfe(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9ed914133e31f69e8796ec059fd9bde69e514367ca54cfe9094376557e60a1(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24fc1c24582c615ad8068c1095c83c5c03e52797bb6bd8a8d47bd2a7ab61107(
    parent: typing.Union[Job, JobCollection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a497289f09f740c75644ac694138b800021e4b73beb111933ed7cc2bf5cdc02c(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa6a8f7c0e607dc2f9e942f39f5f8ad964d6e4f7d906954e89d16169e45b028(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1987c954bc8ff5f11f9b443debf9425852cfee535f0e85d2b79989d428923cf6(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125ab86f0029dcc67ca976ed83fa6db9e9404542d8cae4552e0d4dac0e9891f1(
    scripts: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b23de588de9113dab19ef636449def6cb85f01d84a1a3b15ddf5e35a1b9a189(
    allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4b1d5e688c342aae8b3c5ca41e455b0b73d2c4ead55c8d858977d661f7cc2e(
    artifacts: Artifacts,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b56c55fca73e926648c394ffe52d09ce5bf6e1c066cf53a2c4f6f23a8da51e3(
    cache: Cache,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e49587b212e79c7a8106b2f2a7ca2e46934c763da19022c7f2a8e64400b0a6a(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71deea21d7c27e527b77b8214aafa016d473c5807479aa2efc7d865ef86e07ec(
    image: typing.Union[builtins.str, Image],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40732962652fe2e50d84e53ff922a3dbd8633c1b598ff35d7e393bd6c5786ab2(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb5e14b00eb4e350b88ab4d9f6009226dc17d1e2e8058bca298f098fd88bdca(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f112eb86517c848f04a124efbfe5ad1a61a77053011ed534cbd62b0298f2ef4(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f79da5bb710007e93b0622bb0ca050c33ffe1c2ba0165ae82cf3ba104205ef5(
    stage: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3114d3274dade702f3ea59163b7093cf963a0fc0f5b52deb9548ed497c192006(
    stage: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940f39ed0563dbd5ce1ddd0196a7f0371b0086ce42e8bd3fe034a0b870629473(
    child: typing.Optional[typing.Union[Job, JobCollection]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f410058ae45f87b4744967f654f53c1d4767ecb5a4860e4e045449a2280260bb(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ab7c7bc8d431b6232632429642a5cb932bd7d10f424185811fffcce0247f83(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0ca5bc0e4528b7bf578f909d4c3803e4cb3ba77468906396de9cd5fa3e77c7(
    scripts: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0935cd0552d340f972384e3a86ae9d10ddff13b42b30dd00d9084f480a351c2(
    value: typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdccd2312ed9afe38e1f999efa8e87afb00bf1172a779a57d7bf542f10ef02d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4593026978879fa34fbe85bf848f401a835148b38891be402dd99c6446a6a6bc(
    value: OrderedStringSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464e10f1bf91d67d20ccb380dc46d815aa1e5ef0a935f7f0264179dadc1a4c35(
    value: typing.List[typing.Union[Job, JobCollection]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5171ff36feb8db472dcbfe085f15b589f28a5ae6e733efdabea54894d36f9b0c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819b52d69443a5cfcf420e16e85c1df5ccaf9582385505b81b81a0b71b20c178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a7abfd01c3c0481e3e95bf716cbcb98b2cac85ee4aa21ac4b14b431b005c7b(
    value: typing.Optional[Artifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed9076a7ea726084ecfe53ccd2393796875750aab4677a9d334c0522cd3441d(
    value: typing.Optional[Cache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a5088a4d42d248dff0b622ba0653ee40968fd45e106d98b40c27e729d46cfe(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fea17d587e11eaa0a2f770acaa9f2ac1e06dfbcc89e0755f32ca9c27b9e860(
    value: typing.Optional[Image],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26404ef55b583b637a848e06f3ef983eab5000ac5e9d19c79e43f35c8efb3e8b(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d69ee4b1126a9e6b9d9a678b8b768fc552ab7dde70643963bdef041c4578ba(
    value: typing.Optional[Job],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2609118cc722fb49976ac188e0bb7aea933f6aa6008140e228266700022786(
    value: typing.Optional[typing.List[Rule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa0c5b49599722d0311be14500175639c97eb43d99da3f0b00e5e9eb6e8c6a0(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42da1733be21c876f2b8c557056190aa08f5c8fe3d1d8ae2c892478c8b25944d(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c8f44da804e65c760463d8598c8e5c4ad74285db44713758a3b34104758992(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a15c38332229518ae3150574e93608d030bdc56267bdb62254816ea300c990(
    parent: JobCollection,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f23d98dda585479188e9dcbdd461fcd8989bdb00710a83b9d000bc890223b3(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a07aedddf02b4327d2459c465db8d2c56c742db3d6be14c0627a083ece1600(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8441a024959b5e13a0a59ff2c6c8fc8e59987261a6d2f920a02e78d3c2795e58(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4b8070cd7a2d395a2395131f4d5026555f79f0003e4704e9fcad66ce05342e(
    scripts: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9462d9397982b304d6845e6a714d38a0271b5f25aa7ae896abb85e84a9ded523(
    artifacts: Artifacts,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c5e603d29cd58ae28e444f54de04c88cd13615c3fbc543a1fe6cdae3072da1(
    cache: Cache,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35258a06eebe532433381d99683b8ce812e15b851b60b783cb65f50888732928(
    child: typing.Optional[typing.Union[Job, JobCollection]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed926c1e7c701a185debe51e9806aeb4c1f344d71504a252f886b065b267368e(
    allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de279575d6dfb45a6aa28c525f13751bb58d5d5f8c03225d5b98036a21d40bcc(
    artifacts: Artifacts,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338234c7a7d17c90c76c5eda5a4f4676850ddc78c0a35e52112a5f324519dc9e(
    cache: Cache,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb945393a73d8958d3fc4a5d8fe0b05468aeb7a896e1fd0c9280865d2bcbe97(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc24cbfab1244ecb3fd94133029125b3dcf29d6d1b147b9f5f7e3937024ba6b4(
    image: typing.Union[builtins.str, Image],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fcd9a86bbbad45ce6aaa39fbfac2fb23ede7eae9c6cc49b0dde140061288059(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea4cbe17163697871c2357e3ff5231b092f24931fd8770f8894b2ff56d0daac(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8fd49bc5a9330d7eff9194f17fe23ab926d47e5f632e1f9e61b4e1dcc45d46(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88535091b1345fc77ff978fccb39ce8e9628c0cdd4f16fbc03c571b514065b14(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e90fdcf5ced3e3d3a71ffbec40dcc7c8c9e7c4039d0a74018ebb458e61485ce(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4884ab7cddd84ab13fd45721fecaa391483e6bae522d2a4fdec42b85937fab17(
    allow_failure: typing.Union[builtins.bool, typing.Sequence[jsii.Number]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4638838c6c80a29aaabd27696ad3046a51855ae24e34b0b3c8440a96d369877c(
    dependencies: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d78465bbcbf46c0e9f9b3c8b79e81b590a2e8490887d2a0031b33c4db024825(
    image: typing.Union[builtins.str, Image],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0134a14b49fa583bc5722071b32e2238e1151a607223bbe99189cf1edf4da56(
    needs: typing.Sequence[typing.Union[Job, JobCollection, Need]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04261ac203124b3d169d4d239d34a7d547f8f8e46f5512c85dc2d2f74727996(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d671ef71d13884eeb0dffbed3f512183dca07312902be0ec185079b1ea8a6efd(
    tags: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb5530dd15a5924655ede8b1e1884af69bae49fdd77051ac3c4b35d44306157(
    variables: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5c159d9c5e4c27812c3da4dc97e6e56d1d584af158a50d7b0f284387c7260f(
    rules: typing.Sequence[Rule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7df33f7e535655d2add62cf2ad779e256126fbbd1b9a2b3e9f6080b23ed4447(
    scripts: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d884a03192750ebad3f4984fd76458601b4f922e83e0cde4ee82ea9e40d49b6c(
    value: typing.List[ChildDict],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020fae99a60d2c4b4eacc7370ceafa3ae8de580635c43bbc3e7ad30885f7e304(
    value: OrderedStringSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ce8f87fc09777d997e039769aa954d40880baa7d68702811d01ea13f6ba31d(
    value: OrderedStringSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ccb162d3b020c317be07cba3df0fe16a61ceeb9584d3016f969be36aef5e42a(
    value: OrderedStringSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00f70279d2b723bc21d160de5df77048749cb15e3c5d8bb007b3c102fa2f7e5(
    value: typing.List[typing.Union[Job, JobCollection]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8010f26a7f012891da851efeca7355e695a397fca0f7c558334a2823fc0b0f81(
    value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccb6d32a30dc48a62c971eda38f71296dc661f34966195dcadf95c534940dd3(
    value: typing.Optional[typing.Union[builtins.str, builtins.bool, typing.List[jsii.Number]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0150f47b890e3e8c0aaf17a71490642c1a0f57854515ab728e0a02be72f417(
    value: typing.Optional[Artifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3f56105f78adb7e1d8b7d339e09885a6f5da21efd5d662b12d1caf9cb9d71a(
    value: typing.Optional[Artifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11405e5ad5ee8410ffbcb19fe775c0e9de8028505462748df8772a21d4c7604(
    value: typing.Optional[Artifacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfa065fa29d1dbffd8532c2b4796d8ec0ade220c8029a6a048b53395b0d9e21(
    value: typing.Optional[Cache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bd39e1de9367c6b0bff5bad820b3d65b2e71df866ef37a484a0b76335fb160(
    value: typing.Optional[Cache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee0a9759f2e776c42231317e7d2b7ee3264b893da4c0899cde07f7530631cfc(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5dbc1f13d1b166b200af0d22405b54677a97d49e47c497ebeb9b3a54f8c6d5(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7665c71aaff63d6e2f8516550bf5b26b745d4af6223e82ecb5e80d090ca7dee6(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f864c2feadb144d2585bca7a06e0abacee84879e0047fc313b7a50cea59cccfe(
    value: typing.Optional[typing.Union[builtins.str, Image]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dbe040df39787f521b4ca5c6ba4884183c92369cd61d11482ebc12c95df945(
    value: typing.Optional[typing.Union[builtins.str, Image]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad1158610f11daa642534c94ef06b19443edd5980c3e079e33efdbdab80f8c6(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fefcc9950445b162f148c953f2160becbb8a75ebd8cd86baec8ec42592dea1(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa5cfeee37aa55014cd5ccc7c97fe8d067e69ff8c899926f1fc8607d5ae92b5(
    value: typing.Optional[typing.List[typing.Union[Job, JobCollection, Need]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba39e68be33dd8f847f289aec5d440ca3d90ed3e7fe32ec1a612004f0bf27a1(
    value: typing.Optional[typing.List[Rule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9375709ac002147e2659f0d6ab412b8251e0ca73c9c8d1c7ecc67d9f4aa1c4a(
    value: typing.Optional[typing.List[Rule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd94f3950086c7763e4abda6a3d63b1aaf08d517577753832645b6c3a8fb7ae9(
    value: typing.Optional[typing.List[Rule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144ba7ab97d18f915ade61bb9605b3bb0e29def0712ebfc8d96913dcfcbebc4f(
    value: typing.Optional[typing.List[Rule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d28f2b8a3d9a36e640a646953a54af2370a1c433bc4d837bd61d70a253e4227(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16fd5270e77a60218882f41670ddff30b54e85360e41cc7e9e1d0173c769fc07(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcba7ac6850a2cdf090f3b57395f3a262e6f4e3dc58d6a62c29de6977415737(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b57bc614191724c588f2273cd840e397d88423279b42dffa1f99ede098574a(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5a961f3b0447cab3e54a44811515199806e94203ed2200dd734b1c63aba280(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf71ab3136953b215374020d76f0cc0822594d4e74dc1d4bd715ef1e286d5544(
    stage: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6577d3e2c3ea74e23ec845aaf1ef98de7efaa52a11c10ee3668025ddd828750(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601ddea37bfd612cfd256ac4bbed07e02cfcc3f2b82532c9f110eee789c068d3(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db7b15403a371f7c56c4455186a03d6739aaa4ea519f9d8f10acb8ea445c187(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9f6009e6ceaeb01744958063b9239cf9418bcf6ce43d4f6742d476c7046199(
    child: typing.Optional[typing.Union[Job, JobCollection]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22bb21f984d9a957ce4cd6249b1d3eda009f9fad8470f2a2ed3e33c79818ad5d(
    include: Include,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518219648f52555f1dd663bc1a6d9611e3f2f1791f742920c6a0e72ef4293bdc(
    services: typing.Sequence[Service],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe54c848f938b42878b9e4477e1de81ba9a0eba48c10316fc36700b4194ceb81(
    filename: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbc35e57a5d84ce369bf2bdff03574154554ecb8d1de2885fe78aceeb8a8b19(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4229a956f31df104311d10b187f68bc911b250ae98306d3a832cc2ccb84f0d(
    value: typing.Optional[typing.List[typing.Union[IncludeLocal, IncludeFile, IncludeRemote, IncludeTemplate, IncludeArtifact]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7740e40b673acd58127f23f30a706ffe63e24bfdc90bb4a904118fbcce5bae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0091ce60c1e4494fd202a87f3c771bed351a6d42d9ffc8115b264ec45a598db(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc49353e37d8ad2a0610c6c0b08ce860e0d9b2b9a70ed069768a7483eb608e2(
    excludes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8b4a0edc18e1f688fc2760748dcd456d3534acbf1948a7a776e4f08ee84925(
    paths: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ea9a02de52d1dd351ddd32831cbc225a4799d162305f9f438fe675fe46c3b5(
    comparable: IBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b3ef4ee3502465f1fa2c9802f8541985f1e48407552ea6909dfc2b79c9512c(
    value: OrderedStringSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539fa9abb7f73b7fa20b02adeaeff1784fadc1c06f4f9342be06de91d7f9a313(
    value: OrderedStringSet,
) -> None:
    """Type checking stubs"""
    pass
