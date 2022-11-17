# 2021 created by Sven Rueß, sritd.de
#/omd/sites/BIS/local/lib/python3/cmk/base/plugins/agent_based

from .agent_based_api.v1 import (
	register,
	Service,
	Result,
	State,
	Metric,
	render,
)
from .pure_volumes_performance import (parse_pure_volumes_performance,
							 discovery_pure_volumes_performance)
							 
def parse_pure_volumes(string_table):
	section = {}
	for row in string_table:
		(item, size, total, volumes, data_reduction, total_reduction, shared_space, thin_provisioning, snapshots)  = row

		try:
			size = int(float(size))
		except ValueError:
			size = 0
		try:
			total = int(float(total))
		except ValueError:
			total = 0	
		try:
			volumes = int(float(volumes))
		except ValueError:
			volumes = 0  
		try:
			shared_space = int(float(shared_space))
		except ValueError:
			shared_space = 0
		try:
			thin_provisioning = int(float(thin_provisioning))
		except ValueError:
			thin_provisioning = 0
		try:
			snapshots = int(float(snapshots))
		except ValueError:
			snapshots = 0
		try:
			data_reduction = int(float(data_reduction))
		except ValueError:
			data_reduction = 0
		try:
			total_reduction = int(float(total_reduction))
		except ValueError:
			total_reduction = 0
				

		section[item] = {
			'size': size,
			'total': total,
			'volumes': volumes,
			'data_reduction': data_reduction,
			'total_reduction': total_reduction,
			'shared_space': shared_space,
			'thin_provisioning': thin_provisioning,
			'snapshots': snapshots,
		}
	return section

register.agent_section(
	name="pure_volumes",
	parse_function=parse_pure_volumes,
)

def discovery_pure_volumes(section):
	for item in section.keys():
		yield Service(item=item)

def check_pure_volumes(item, section):
	failed = []

	if item not in section.keys():
		yield Result(
			state=State.UNKNOWN,
			summary=f"Item {item} not found",
		)
		
	data = section[item]

	sizesum = f"{int(float(data['size']))}"
	totalsum = f"{int(float(data['total']))}"
	pervolume_total_percent= (int(totalsum) / int(sizesum))
	pervolume_total_free= (int(float(sizesum)) - int(float(totalsum)))
	percentage_total = f"{pervolume_total_percent:.0%}"
	
	if section[item]['snapshots'] == 'empty':
		yield Result(
			state=State.CRIT,
			summary=f"CRIT, size: {render.bytes(data['size'])}, used: {render.bytes(data['total'])}, free: {render.bytes(pervolume_total_free)}, percent in use: {percentage_total}",
			details=f"Data Reduction: {data['data_reduction']} to 1, Total reduction: {(data['total_reduction'])} to 1, Shared Space: {render.bytes(data['shared_space'])}, Thin Provisioned: {data['thin_provisioning']}, Snapshots: {render.bytes(data['snapshots'])}, Used after deduplication: {render.bytes(data['volumes'])}",
		)
	else:
		yield Result(
			state=State.OK,
			summary=f"OK, size: {render.bytes(data['size'])}, used: {render.bytes(data['total'])}, free: {render.bytes(pervolume_total_free)}, percent in use: {percentage_total}",
			details=f"Data Reduction: {data['data_reduction']} to 1, Total reduction: {(data['total_reduction'])} to 1, Shared Space: {render.bytes(data['shared_space'])}, Thin Provisioned: {data['thin_provisioning']}, Snapshots: {render.bytes(data['snapshots'])}, Used after deduplication: {render.bytes(data['volumes'])}",
		)

register.check_plugin(
	name="pure_volumes",
	sections=['pure_volumes'],	
	service_name="volume %s",
	discovery_function=discovery_pure_volumes,
	check_function=check_pure_volumes,
)