'''
[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-responsive-email-template

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-responsive-email-template)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-responsive-email-template/)

> Responsive [mjml](https://documentation.mjml.io/) email template for aws ses

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-responsive-email-template
```

Python:

```bash
pip install cloudcomponents.cdk-responsive-email-template
```

## How to use

```python
import { ResponsiveEmailTemplate, TemplatePart } from '@cloudcomponents/cdk-responsive-email-template';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';

export class ResponsiveEmailTemplateStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);

    new ResponsiveEmailTemplate(this, 'EmailTemplate', {
      templateName: 'demo',
      subjectPart: 'cloudcomponents - {{ title }}',
      textPart: TemplatePart.fromInline('text message'),
      htmlPart: TemplatePart.fromInline(`<mjml>
    <mj-head>
      <mj-title>cloudcomponents - {{ title }}</mj-title>
    </mj-head>
    <mj-body>
      <mj-section>
        <mj-column>
          <mj-text>
            Hello {{ name }}!
          </mj-text>
        </mj-column>
      </mj-section>
    </mj-body>
  </mjml>`),
      parsingOptions: {
        beautify: true,
      },
    });
  }
}
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-responsive-email-template/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-responsive-email-template/LICENSE)
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

import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-responsive-email-template.ParsingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "beautify": "beautify",
        "file_path": "filePath",
        "fonts": "fonts",
        "keep_comments": "keepComments",
        "minify": "minify",
        "mjml_config_path": "mjmlConfigPath",
        "validation_level": "validationLevel",
    },
)
class ParsingOptions:
    def __init__(
        self,
        *,
        beautify: typing.Optional[builtins.bool] = None,
        file_path: typing.Optional[builtins.str] = None,
        fonts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        keep_comments: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        mjml_config_path: typing.Optional[builtins.str] = None,
        validation_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param beautify: Option to beautify the HTML output. Default: : false
        :param file_path: Full path of the specified file to use when resolving paths from mj-include components. Default: : templateDir or '.'
        :param fonts: Default fonts imported in the HTML rendered by HTML ie. { 'Open Sans': 'https://fonts.googleapis.com/css?family=Open+Sans:300,400,500,700' } Default: :
        :param keep_comments: Option to keep comments in the HTML output. Default: : true
        :param minify: Option to minify the HTML output. Default: : false
        :param mjml_config_path: The path or directory of the .mjmlconfig file default: process.cwd().
        :param validation_level: How to validate your MJML. skip: your document is rendered without going through validation soft: your document is going through validation and is rendered, even if it has errors strict: your document is going through validation and is not rendered if it has any error Default: : soft
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8195bad39348d44a2703c9449e695773351d68d6f0d4f37224a16c62c6f2f7df)
            check_type(argname="argument beautify", value=beautify, expected_type=type_hints["beautify"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
            check_type(argname="argument fonts", value=fonts, expected_type=type_hints["fonts"])
            check_type(argname="argument keep_comments", value=keep_comments, expected_type=type_hints["keep_comments"])
            check_type(argname="argument minify", value=minify, expected_type=type_hints["minify"])
            check_type(argname="argument mjml_config_path", value=mjml_config_path, expected_type=type_hints["mjml_config_path"])
            check_type(argname="argument validation_level", value=validation_level, expected_type=type_hints["validation_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if beautify is not None:
            self._values["beautify"] = beautify
        if file_path is not None:
            self._values["file_path"] = file_path
        if fonts is not None:
            self._values["fonts"] = fonts
        if keep_comments is not None:
            self._values["keep_comments"] = keep_comments
        if minify is not None:
            self._values["minify"] = minify
        if mjml_config_path is not None:
            self._values["mjml_config_path"] = mjml_config_path
        if validation_level is not None:
            self._values["validation_level"] = validation_level

    @builtins.property
    def beautify(self) -> typing.Optional[builtins.bool]:
        '''Option to beautify the HTML output.

        :default: : false
        '''
        result = self._values.get("beautify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def file_path(self) -> typing.Optional[builtins.str]:
        '''Full path of the specified file to use when resolving paths from mj-include components.

        :default: : templateDir or '.'
        '''
        result = self._values.get("file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fonts(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Default fonts imported in the HTML rendered by HTML ie.

        { 'Open Sans': 'https://fonts.googleapis.com/css?family=Open+Sans:300,400,500,700' }

        :default: :

        :see: https://github.com/mjmlio/mjml/blob/master/packages/mjml-core/src/index.js
        '''
        result = self._values.get("fonts")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def keep_comments(self) -> typing.Optional[builtins.bool]:
        '''Option to keep comments in the HTML output.

        :default: : true
        '''
        result = self._values.get("keep_comments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify(self) -> typing.Optional[builtins.bool]:
        '''Option to minify the HTML output.

        :default: : false
        '''
        result = self._values.get("minify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mjml_config_path(self) -> typing.Optional[builtins.str]:
        '''The path or directory of the .mjmlconfig file default: process.cwd().'''
        result = self._values.get("mjml_config_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validation_level(self) -> typing.Optional[builtins.str]:
        '''How to validate your MJML.

        skip: your document is rendered without going through validation
        soft: your document is going through validation and is rendered, even if it has errors
        strict: your document is going through validation and is not rendered if it has any error

        :default: : soft
        '''
        result = self._values.get("validation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParsingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ResponsiveEmailTemplate(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-responsive-email-template.ResponsiveEmailTemplate",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        html_part: "TemplatePart",
        subject_part: builtins.str,
        template_name: builtins.str,
        parsing_options: typing.Optional[typing.Union[ParsingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        text_part: typing.Optional["TemplatePart"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param html_part: -
        :param subject_part: -
        :param template_name: -
        :param parsing_options: -
        :param text_part: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305f6ada7e7b0a0cfddd30be9a30b191b5cbf3941451252f99a48a808f5be00e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ResponsiveEmailTemplateProps(
            html_part=html_part,
            subject_part=subject_part,
            template_name=template_name,
            parsing_options=parsing_options,
            text_part=text_part,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-responsive-email-template.ResponsiveEmailTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "html_part": "htmlPart",
        "subject_part": "subjectPart",
        "template_name": "templateName",
        "parsing_options": "parsingOptions",
        "text_part": "textPart",
    },
)
class ResponsiveEmailTemplateProps:
    def __init__(
        self,
        *,
        html_part: "TemplatePart",
        subject_part: builtins.str,
        template_name: builtins.str,
        parsing_options: typing.Optional[typing.Union[ParsingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        text_part: typing.Optional["TemplatePart"] = None,
    ) -> None:
        '''
        :param html_part: -
        :param subject_part: -
        :param template_name: -
        :param parsing_options: -
        :param text_part: -
        '''
        if isinstance(parsing_options, dict):
            parsing_options = ParsingOptions(**parsing_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70fddcab7c0b1a977a9447819c045132288be9753806ddc6aa3829cc3aa6266)
            check_type(argname="argument html_part", value=html_part, expected_type=type_hints["html_part"])
            check_type(argname="argument subject_part", value=subject_part, expected_type=type_hints["subject_part"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument parsing_options", value=parsing_options, expected_type=type_hints["parsing_options"])
            check_type(argname="argument text_part", value=text_part, expected_type=type_hints["text_part"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "html_part": html_part,
            "subject_part": subject_part,
            "template_name": template_name,
        }
        if parsing_options is not None:
            self._values["parsing_options"] = parsing_options
        if text_part is not None:
            self._values["text_part"] = text_part

    @builtins.property
    def html_part(self) -> "TemplatePart":
        result = self._values.get("html_part")
        assert result is not None, "Required property 'html_part' is missing"
        return typing.cast("TemplatePart", result)

    @builtins.property
    def subject_part(self) -> builtins.str:
        result = self._values.get("subject_part")
        assert result is not None, "Required property 'subject_part' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_name(self) -> builtins.str:
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parsing_options(self) -> typing.Optional[ParsingOptions]:
        result = self._values.get("parsing_options")
        return typing.cast(typing.Optional[ParsingOptions], result)

    @builtins.property
    def text_part(self) -> typing.Optional["TemplatePart"]:
        result = self._values.get("text_part")
        return typing.cast(typing.Optional["TemplatePart"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResponsiveEmailTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TemplatePart(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cloudcomponents/cdk-responsive-email-template.TemplatePart",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromFile")
    @builtins.classmethod
    def from_file(cls, file_path: builtins.str) -> "TemplatePart":
        '''
        :param file_path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45db1587c1043d5390ae334ad64a6bfe69a54b6230f34a21377136fc7cbce356)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast("TemplatePart", jsii.sinvoke(cls, "fromFile", [file_path]))

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, source: builtins.str) -> "TemplatePart":
        '''
        :param source: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a0bdb1b7c604e9c31386689c15a29ad75b0880f9bc0a46a144bc6fc4110232c)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        return typing.cast("TemplatePart", jsii.sinvoke(cls, "fromInline", [source]))

    @builtins.property
    @jsii.member(jsii_name="source")
    @abc.abstractmethod
    def source(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultFilePath")
    @abc.abstractmethod
    def default_file_path(self) -> typing.Optional[builtins.str]:
        ...


class _TemplatePartProxy(TemplatePart):
    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="defaultFilePath")
    def default_file_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultFilePath"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TemplatePart).__jsii_proxy_class__ = lambda : _TemplatePartProxy


__all__ = [
    "ParsingOptions",
    "ResponsiveEmailTemplate",
    "ResponsiveEmailTemplateProps",
    "TemplatePart",
]

publication.publish()

def _typecheckingstub__8195bad39348d44a2703c9449e695773351d68d6f0d4f37224a16c62c6f2f7df(
    *,
    beautify: typing.Optional[builtins.bool] = None,
    file_path: typing.Optional[builtins.str] = None,
    fonts: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    keep_comments: typing.Optional[builtins.bool] = None,
    minify: typing.Optional[builtins.bool] = None,
    mjml_config_path: typing.Optional[builtins.str] = None,
    validation_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305f6ada7e7b0a0cfddd30be9a30b191b5cbf3941451252f99a48a808f5be00e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    html_part: TemplatePart,
    subject_part: builtins.str,
    template_name: builtins.str,
    parsing_options: typing.Optional[typing.Union[ParsingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    text_part: typing.Optional[TemplatePart] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70fddcab7c0b1a977a9447819c045132288be9753806ddc6aa3829cc3aa6266(
    *,
    html_part: TemplatePart,
    subject_part: builtins.str,
    template_name: builtins.str,
    parsing_options: typing.Optional[typing.Union[ParsingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    text_part: typing.Optional[TemplatePart] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45db1587c1043d5390ae334ad64a6bfe69a54b6230f34a21377136fc7cbce356(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0bdb1b7c604e9c31386689c15a29ad75b0880f9bc0a46a144bc6fc4110232c(
    source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
