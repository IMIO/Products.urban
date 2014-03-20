# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
from Products.urban.content.interfaces import IArchitect

from Products.urban.cfg import interfaces as cfg_interfaces
IUrbanTool = cfg_interfaces.IUrbanTool

class IProprietary(Interface):
    """Marker interface for .Proprietary.Proprietary
    """


class IApplicant(Interface):
    """Marker interface for .Applicant
    """


CONTACT_INTERFACES = {
    'Applicant': IApplicant,
    'Architect': IArchitect,
    # 'Notary' : INotary,  # to be taken into account if notary.py is removed
    # 'Proprietary' : IProprietary, # to be taken into account if proprietary.py is removed
}

##/code-section HEAD

class IGenericLicence(Interface):
    """Marker interface for .GenericLicence.GenericLicence
    """

class IBuildLicence(Interface):
    """Marker interface for .BuildLicence.BuildLicence
    """

class IParcelOutLicence(Interface):
    """Marker interface for .ParcelOutLicence.ParcelOutLicence
    """

class ILayer(Interface):
    """Marker interface for .Layer.Layer
    """

class IDeclaration(Interface):
    """Marker interface for .Declaration.Declaration
    """

class IUrbanCertificateBase(Interface):
    """Marker interface for .UrbanCertificateBase.UrbanCertificateBase
    """

class IUrbanCertificateTwo(Interface):
    """Marker interface for .UrbanCertificateTwo.UrbanCertificateTwo
    """

class IDivision(Interface):
    """Marker interface for .Division.Division
    """

class IMiscDemand(Interface):
    """Marker interface for .MiscDemand.MiscDemand
    """

class IEnvironmentBase(Interface):
    """Marker interface for .EnvironmentBase.EnvironmentBase
    """

class IEnvironmentLicence(Interface):
    """Marker interface for .EnvironmentLicence.EnvironmentLicence
    """

##code-section FOOT
class ILicenceContainer(Interface):
    """
    Marker interface for a folder containing Licences
    """


class IUrbanBase(Interface):
    """Marker interface for .Base.UrbanBase
    """


class IUrbanCertificateOne(Interface):
    """Marker interface for UrbanCertificateOne
    """


class INotaryLetter(Interface):
    """Marker interface for EnvClassThree
    """


class IEnvClassThree(Interface):
    """Marker interface for EnvClassThree
    """

class IEnvCLassOne(Interface):
    """Marker interface for .EnvClassOne
    """


class IContactFolder(Interface):
    """Marker interface for folders containing contacts
    """

##/code-section FOOT
