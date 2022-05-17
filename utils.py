from pathlib import Path
import shutil
import typing

import SimpleITK as sitk
import pydicom
from pydicom import dcmread

dcm_tags_to_check: dict = {'Modality': 'CT',
                           'BodyPartExamined': 'HEAD'}
image_type_ = "AXIAL"


def get_qualified_series_id_for_study(study_path: Path, min_dcm_files: int = 10) -> typing.List[str]:
    qualified = list()
    if study_path.is_dir():
        series_ids = sitk.ImageSeriesReader.GetGDCMSeriesIDs(str(study_path))
        for sid in series_ids:
            series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(str(study_path), sid)
            dcm_file = dcmread(series_file_names[0], stop_before_pixels=True)

            conditions = list()
            for tag in dcm_tags_to_check:
                conditions.append(eval('dcm_file.' + tag + '.upper()') == dcm_tags_to_check[tag].upper())
            conditions.append(image_type_.upper() in [i.upper() for i in dcm_file.ImageType])
            conditions.append(len(series_file_names) >= min_dcm_files)

            if all(conditions):
                # print(
                #     f'series {sid} in study {study_path} is a CT-Head series with {len(series_file_names)} dicom files')
                qualified.append(sid)
    return qualified


def anonymize(dataset: pydicom.Dataset):
    def person_names_callback(dataset, data_element):
        if data_element.VR == "PN":
            data_element.value = "anonymous"

    def curves_callback(dataset, data_element):
        if data_element.tag.group & 0xFF00 == 0x5000:
            del dataset[data_element.tag]

    dataset.PatientID = "id"
    dataset.walk(person_names_callback)
    dataset.walk(curves_callback)

def delete_folder_content(folder: Path):
    for file_path in folder.iterdir():
        try:
            if file_path.is_file() or file_path.is_symlink():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
