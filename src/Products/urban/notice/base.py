# -*- coding: utf-8 -*-


class NoticeElement(object):
    _notice_keys = ()  # List of attributes that are usefull but specific to notice
    _excluded_keys = ()  # List of attributes that should be not included

    def _get_data(self, *keys):
        """Method to get informations from json raw data"""
        data = self.json
        for key in keys:
            if not data:
                return
            if isinstance(data, dict):
                if key not in data:
                    return
            elif isinstance(data, list):
                if not isinstance(key, int):
                    return
                if len(data) < key + 1:
                    return
            data = data[key]
        return data

    def serialize(self):
        """Return a dictionary with data"""
        excluded_keys = (
            ("serialize", "json", "service") + self._notice_keys + self._excluded_keys
        )
        result = {}
        for key in [
            k for k in dir(self) if k not in excluded_keys and not k.startswith("_")
        ]:
            value = getattr(self, key)
            if isinstance(value, list):
                if value and isinstance(value[0], NoticeElement):
                    value = [v.serialize() for v in value]
            elif isinstance(value, string_types):
                value = value.strip()
            if value is not None:
                result[key] = value
        return result
