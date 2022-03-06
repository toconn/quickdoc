#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class AppInfo:
	name: str
	version: str
	created_date: str
	build_date: str
	build_number: str
