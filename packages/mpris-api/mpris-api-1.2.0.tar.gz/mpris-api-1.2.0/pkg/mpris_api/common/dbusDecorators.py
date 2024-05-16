#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import inspect
from typing import Callable, Sequence, TypeVar

from dbus_next.service import dbus_property, method, signal

from mpris_api.common.DbusPrimitive import DbusPrimitive
from mpris_api.common.DbusType import IDbusType

dbusSignal = signal
dbusProperty = dbus_property
dbusMethod = method


TReturn = TypeVar('TReturn')


class DbusSignatureMismatch(TypeError):
    pass


def dbusInterfaceSignature(
    argTypes: Sequence[IDbusType],
    returnType: IDbusType = DbusPrimitive.NOTHING
) -> Callable[..., Callable[..., TReturn]]:
    def decorator(func: Callable[..., TReturn]) -> Callable[..., TReturn]:
        signatureOrg = inspect.signature(func)

        paramsOrg = list(signatureOrg.parameters.values())
        if len(paramsOrg) != (len(argTypes) + 1):
            raise DbusSignatureMismatch(f'Parameter count mismatch! func="{func.__name__}"')

        paramsNew = [paramsOrg[0]]
        for index, (param, dbusType) in enumerate(zip(paramsOrg[1:], argTypes)):
            paramTypeOrg = param.annotation
            paramTypeCheck = dbusType.getSignaturePy()
            if paramTypeOrg != paramTypeCheck:
                raise DbusSignatureMismatch(f'Parameter {index} type mismatch! "{paramTypeOrg}"!="{paramTypeCheck}"')

            paramsNew.append(param.replace(annotation=dbusType.getSignatureDbus()))

        returnTypeOrg = signatureOrg.return_annotation
        returnTypeCheck = returnType.getSignaturePy()
        if returnTypeOrg != returnTypeCheck:
            raise DbusSignatureMismatch(f'Return type mismatch! "{returnTypeOrg}"!="{returnTypeCheck}"')

        signatureNew = signatureOrg.replace(parameters=paramsNew, return_annotation=returnType.getSignatureDbus())
        setattr(func, '__signature__', signatureNew)

        return func

    return decorator
