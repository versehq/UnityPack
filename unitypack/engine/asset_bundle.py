﻿from enum import IntEnum
from .component import Component
from .object import Object, field, field_list, field_dict
#from unitypack.object import ObjectPointer
import json

class AssetInfo(Object):
	preloadIndex = field("preloadIndex", int)
	preloadSize = field("preloadSize", int)
	asset = field("asset")

class AssetBundle(Object):
	m_PreloadTable = field_list("m_PreloadTable")
	m_Container = field_dict("m_Container", str, AssetInfo)
	m_MainAsset = field("m_MainAsset", AssetInfo)
	m_AssetBundleName = field("m_AssetBundleName")
	m_Dependencies = field("m_Dependencies")

	def __str__(self):
		return self.name

	def to_json_data(self, asset_bundle_obj):
		bundle = asset_bundle_obj.asset.bundle
		block_storage_file_offset = 0
		if bundle is not None:
			block_storage_file_offset = bundle.block_storage_file_offset

		this_json_data = ({
			'name': self.name,
			'AssetBundleName': self.m_AssetBundleName,
			'Dependencies': self.m_Dependencies,
		})

		container_dict = {}
		for path, asset_info in self.m_Container.items():
			obj_ptr = asset_info.asset
			if obj_ptr is None:
				print("No 'asset' value for {0}".format(path))
				continue;

			obj = obj_ptr.object
			value = ({
					'PathId': obj_ptr.path_id,
					'UnityType': obj.type,
					'Size': obj.size,
					'OffsetInBlock': obj.data_offset,
					'OffsetInFile': block_storage_file_offset + obj.data_offset,
				})

			if path in container_dict:
				existing_value = container_dict[path]
				print("Found duplicate of {0}".format(path))
				print("Existing: " + json.dumps(existing_value))
				print("Duplicate: " + json.dumps(value))
				print()
				continue

			container_dict[path] = value

		this_json_data['Assets'] = container_dict

		return this_json_data
