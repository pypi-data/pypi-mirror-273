import random
from datetime import datetime

from pydicom import Dataset, read_file, uid

from .IOD import IOD, IODTypes, SOP_CLASS_UID_MODALITY_DICT
from .modules.specific_sr_modules import SRDocumentSeriesModule, SRDocumentGeneralModule
from .modules.specific_sr_modules import SRDocumentContentModule
from .sequences.Sequences import (
    generate_sequence,
    generate_CRPES_sequence,
    update_and_insert_additional_DICOM_attributes_in_ds,
)
from .sequences.Sequences import generate_reference_sop_sequence_json


class EnhancedSRTID4300(IOD):
    """Implementation of the Enhanced SR IOD using Template ID 1500"""

    def __init__(self):
        super().__init__(IODTypes.EnhancedSR)

    def create_empty_iod(self):
        """Creates an empty IOD of type Enhanced SR"""
        super().create_empty_iod()
        self.copy_required_dicom_attributes(Dataset(), include_optional=True)

    def copy_required_dicom_attributes(
        self, dataset_to_copy_from, include_iod_specific=True, include_optional=False
    ):
        """Copies required DICOM attributes from provided dataset
        Parameters
        ----------
        dataset_to_copy_from : Dataset to copy DICOM attributes from
        include_iod_specific : Include IOD specific DICOM attributes in copy (True)
        include_optional : Include optional DICOM attributes in copy (False)
        """
        super().copy_required_dicom_attributes(dataset_to_copy_from, include_optional)

        if include_iod_specific:
            sr_specific_modules = [
                SRDocumentSeriesModule(),
                SRDocumentGeneralModule(),
                SRDocumentContentModule(),
            ]
            for module in sr_specific_modules:
                module.copy_required_dicom_attributes(
                    dataset_to_copy_from, self.dataset
                )
                if include_optional:
                    module.copy_optional_dicom_attributes(
                        dataset_to_copy_from, self.dataset
                    )

    def initiate(self, referenced_dcm_files=None):
        """Initiate the IOD by setting some dummy values for required attributes

        Keyword Arguments:
            referenced_dcm_files {[dcm_file1, dcm_file2, ...]} -- List of file paths (default: {None})
        """
        super().initiate()
        if referenced_dcm_files:
            # some attributes to inherit from referenced dcm files
            ds = read_file(referenced_dcm_files[0])
            self.dataset.PatientID = ds.PatientID
            self.dataset.PatientName = ds.PatientName
            self.dataset.PatientSex = ds.PatientSex
            self.dataset.PatientBirthDate = (
                ds.PatientBirthDate if "PatientBirthDate" in ds else ""
            )
            self.dataset.StudyInstanceUID = ds.StudyInstanceUID
            self.dataset.StudyID = ds.StudyID
            self.dataset.AccessionNumber = ds.AccessionNumber
            if "StudyDescription" in ds:
                self.dataset.StudyDescription = ds.StudyDescription
            self.dataset.StudyDate = ds.StudyDate
            self.dataset.StudyTime = ds.StudyTime
        # sr document series module
        self.dataset.Modality = SOP_CLASS_UID_MODALITY_DICT[self.iod_type]
        self.dataset.SeriesInstanceUID = uid.generate_uid()
        # sr document general module
        self.dataset.InstanceNumber = str(1)
        self.dataset.CompletionFlag = "COMPLETE"
        self.dataset.VerificationFlag = "UNVERIFIED"
        self.dataset.ContentDate = datetime.now().strftime("%Y%m%d")
        self.dataset.ContentTime = datetime.now().strftime("%H%M%S")
        if referenced_dcm_files:
            self.dataset.CurrentRequestedProcedureEvidenceSequence = (
                generate_CRPES_sequence(referenced_dcm_files)
            )
        self.dataset.PreliminaryFlag = "FINAL"
        # sr document content module
        self.dataset.ValueType = "CONTAINER"
        self.dataset.ConceptNameCodeSequence = generate_sequence(
            "ConceptNameCodeSequence",
            [
                {
                    "CodeValue": "126000",
                    "CodingSchemeDesignator": "DCM",
                    "CodeMeaning": "Imaging Measurement Report",
                }
            ],
        )
        self.dataset.ContentTemplateSequence = generate_sequence(
            "ContentTemplateSequence",
            [
                {
                    "MappingResource": "DCMR",
                    "MappingResourceUID": "1.2.840.10008.8.1.1",
                    "TemplateIdentifier": "4300",
                }
            ],
        )
        self.dataset.ContinuityOfContent = "SEPARATE"
        self.dataset.ContentSequence = generate_sequence(
            "ContentSequence",
            [
                {
                    "RelationshipType": "HAS CONCEPT MOD",
                    "ValueType": "CODE",
                    "ConceptNameCodeSequence": [
                        {
                            "CodeValue": "121049",
                            "CodingSchemeDesignator": "DCM",
                            "CodeMeaning": "Language of Content Item and Descendants",
                        }
                    ],
                    "ConceptCodeSequence": [
                        {
                            "CodeValue": "eng",
                            "CodingSchemeDesignator": "RFC5646",
                            "CodeMeaning": "English",
                        }
                    ],
                    "ContentSequence": [
                        {
                            "RelationshipType": "HAS CONCEPT MOD",
                            "ValueType": "CODE",
                            "ConceptNameCodeSequence": [
                                {
                                    "CodeValue": "121046",
                                    "CodingSchemeDesignator": "DCM",
                                    "CodeMeaning": "Country of Language",
                                }
                            ],
                            "ConceptCodeSequence": [
                                {
                                    "CodeValue": "US",
                                    "CodingSchemeDesignator": "ISO3166_1",
                                    "CodeMeaning": "United States",
                                }
                            ],
                        }
                    ],
                },
                {
                    "RelationshipType": "CONTAINS",
                    "ValueType": "CODE",
                    "ConceptNameCodeSequence": [
                        {
                            "CodeValue": "130551",
                            "CodingSchemeDesignator": "DCM",
                            "CodeMeaning": "Reporting system",
                        }
                    ],
                    "ConceptCodeSequence": [
                        {
                            "CodeValue": "130564",
                            "CodingSchemeDesignator": "DCM",
                            "CodeMeaning": "PI-RADS v2.1",
                        }
                    ],
                },
                {
                    "RelationshipType": "CONTAINS",
                    "ValueType": "CONTAINER",
                    "ConceptNameCodeSequence": [
                        {
                            "CodeValue": "111028",
                            "CodingSchemeDesignator": "DCM",
                            "CodeMeaning": "Image Library",
                        }
                    ],
                    "ContinuityOfContent": "SEPARATE",
                    "ContentSequence": [
                        {
                            "RelationshipType": "CONTAINS",
                            "ValueType": "CONTAINER",
                            "ConceptNameCodeSequence": [
                                {
                                    "CodeValue": "126200",
                                    "CodingSchemeDesignator": "DCM",
                                    "CodeMeaning": "Image Library Group",
                                }
                            ],
                            "ContinuityOfContent": "SEPARATE",
                            "ContentSequence": [
                                generate_reference_sop_sequence_json(dcm_file)
                                for dcm_file in referenced_dcm_files
                            ],
                        }
                    ],
                },
                # CONTAINS TID 9007 - General Relevant Patient Information (U)
                # CONTAINS 130552 DCM Prostate MRI relevant procedure information (U)
                # TID 3106 Drugs/Contrast Administered (U)
                # CODE 130543 DCM Endorectal coil used (U)
                # CONTAINS TID 1701 Imaging Study Quality (U)
                # CONTAINS TID 4203 Prostate Imaging Findings
                {
                    "RelationshipType": "CONTAINS",
                    "ValueType": "CONTAINER",
                    "ConceptNameCodeSequence": [
                        {
                            "CodeValue": "130553",
                            "CodingSchemeDesignator": "DCM",
                            "CodeMeaning": "Prostate Imaging Findings",
                        }
                    ],
                    "ContinuityOfContent": "SEPARATE",
                    "ContentSequence": [],
                },
            ],
        )

    def add_observation_context(self):
        ds = Dataset()
        ds.RelationshipType = "HAS OBS CONTEXT"
        ds.ValueType = "INCLUDE"
        ds.ContentSequence = generate_sequence(
            "ContentSequence",
            [
                {
                    "ValueType": "CONTAINER",
                    "ConceptNameCodeSequence": {
                        "CodeValue": "121049",
                        "CodingSchemeDesignator": "DCM",
                        "CodeMeaning": "Observation Context",
                    },
                    "ContinuityOfContent": "SEPARATE",
                    "ContentSequence": [
                        {
                            "ValueType": "CODE",
                            "ConceptNameCodeSequence": {
                                "CodeValue": "121005",
                                "CodingSchemeDesignator": "DCM",
                                "CodeMeaning": "Observer Type",
                            },
                            "ContentCodeSequence": {
                                "CodeValue": "121006",
                                "CodingSchemeDesignator": "DCM",
                                "CodeMeaning": "Person",
                            },
                        },
                        {
                            "ValueType": "PNAME",
                            "ConceptNameCodeSequence": {
                                "CodeValue": "121008",
                                "CodingSchemeDesignator": "DCM",
                                "CodeMeaning": "Person Observer Name",
                            },
                            "PersonName": "Dr. Observer",
                        },
                        {
                            "ValueType": "CODE",
                            "ConceptNameCodeSequence": {
                                "CodeValue": "121005",
                                "CodingSchemeDesignator": "DCM",
                                "CodeMeaning": "Observer Type",
                            },
                            "ContentCodeSequence": {
                                "CodeValue": "121007",
                                "CodingSchemeDesignator": "DCM",
                                "CodeMeaning": "Device",
                            },
                        },
                        {
                            "ValueType": "TEXT",
                            "ConceptNameCodeSequence": {
                                "CodeValue": "121012",
                                "CodingSchemeDesignator": "DCM",
                                "CodeMeaning": "Device Observer Identifier",
                            },
                            "TextValue": "Device123",
                        },
                    ],
                }
            ],
        )
        self.dataset.ContentSequence.append(ds)

    def add_time_point_context(self):
        ds = Dataset()
        ds.RelationshipType = "HAS OBS CONTEXT"
        ds.ValueType = "INCLUDE"
        ds.ContentSequence = generate_sequence(
            "ContentSequence",
            [
                {
                    "ValueType": "CONTAINER",
                    "ConceptNameCodeSequence": {
                        "CodeValue": "126010",
                        "CodingSchemeDesignator": "DCM",
                        "CodeMeaning": "Time Point Context",
                    },
                    "ContinuityOfContent": "SEPARATE",
                    "ContentSequence": [
                        {
                            "ValueType": "TEXT",
                            "ConceptNameCodeSequence": {
                                "CodeValue": "111700",
                                "CodingSchemeDesignator": "DCM",
                                "CodeMeaning": "Time Point Identifier",
                            },
                            "TextValue": "TP1",
                        },
                        {
                            "ValueType": "TEXT",
                            "ConceptNameCodeSequence": {
                                "CodeValue": "111701",
                                "CodingSchemeDesignator": "DCM",
                                "CodeMeaning": "Time Point Description",
                            },
                            "TextValue": "Baseline",
                        },
                    ],
                }
            ],
        )
        self.dataset.ContentSequence.append(ds)

    def add_overall_prostate_finding(
        self,
        tracking_id,
        tracking_uid,
        finding=("255503000", "SCT", "Entire"),
        finding_site=("41216001", "SCT", "Prostate"),
    ):
        if not tracking_id:
            tracking_id = "".join(random.choice("0123456789ABCDEF") for i in range(16))
        if not tracking_uid:
            tracking_uid = uid.generate_uid()
        ds = Dataset()
        ds.RelationshipType = "CONTAINS"
        ds.ValueType = "CONTAINER"
        ds.ConceptNameCodeSequence = generate_sequence(
            "ConceptNameCodeSequence",
            [
                [
                    {
                        "CodeValue": "130554",
                        "CodingSchemeDesignator": "DCM",
                        "CodeMeaning": "Overall Prostate Finding",
                    }
                ]
            ],
        )
        ds.ContinuityOfContent = "SEPARATE"
        ds.ContentSequence = generate_sequence(
            "ContentSequence",
            [
                {
                    "RelationshipType": "HAS OBS CONTEXT",
                    "ValueType": "TEXT",
                    "ConceptNameCodeSequence": [
                        {
                            "CodeValue": "112039",
                            "CodingSchemeDesignator": "DCM",
                            "CodeMeaning": "Tracking Identifier",
                        }
                    ],
                    "TextValue": tracking_id,
                },
                {
                    "RelationshipType": "HAS OBS CONTEXT",
                    "ValueType": "UIDREF",
                    "ConceptNameCodeSequence": [
                        {
                            "CodeValue": "112040",
                            "CodingSchemeDesignator": "DCM",
                            "CodeMeaning": "Tracking Unique Identifier",
                        }
                    ],
                    "UID": tracking_uid,
                },
                {
                    "RelationshipType": "CONTAINS",
                    "ValueType": "CODE",
                    "ConceptNameCodeSequence": [
                        {
                            "CodeValue": "121071",
                            "CodingSchemeDesignator": "DCM",
                            "CodeMeaning": "Finding",
                        }
                    ],
                    "ConceptCodeSequence": [
                        {
                            "CodeValue": finding[0],
                            "CodingSchemeDesignator": finding[1],
                            "CodeMeaning": finding[2],
                        }
                    ],
                },
                {
                    "RelationshipType": "HAS CONCEPT MOD",
                    "ValueType": "CODE",
                    "ConceptNameCodeSequence": [
                        {
                            "CodeValue": "363698007",
                            "CodingSchemeDesignator": "SCT",
                            "CodeMeaning": "Finding Site",
                        }
                    ],
                    "ConceptCodeSequence": [
                        {
                            "CodeValue": finding_site[0],
                            "CodingSchemeDesignator": finding_site[1],
                            "CodeMeaning": finding_site[2],
                        }
                    ],
                },
            ],
        )
        self.dataset.ContentSequence.append(ds)

    def add_localized_prostate_finding(self):
        pass

    def add_exptra_prostate_finding(self):
        pass
