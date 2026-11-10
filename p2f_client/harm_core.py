# Local libraries
from p2f_pydantic.harm_core import Core, CoreSegment
# Third Party Libraries
from .conn import eval_non_ok_return
# Batteries included libraries
from uuid import UUID
from typing import Optional, List, Literal

class harm_core:
    def __init__(self, p2fclient):
        self.p2fclient = p2fclient
        self.base_url = p2fclient.base_url
        self.prefix = "harm-core/"
        self.core_url = self.base_url / self.prefix
        self.data_model_Core = Core
        self.data_model_CoreSegment = CoreSegment
    def upload_core(self, new_core: Core) -> Core:
        """Upload a HARM Core to the API

        :param new_core: Core object to be uploaded
        :type new_core: Core
        :return: Core object as processed by server
        :rtype: Core
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.post(self.core_url, 
                                data=new_core.model_dump_json(exclude_unset=True))
                if r.ok:
                    return Core(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def upload_core_segment(self,
                            core_id: UUID, 
                            new_core_segment: CoreSegment) -> CoreSegment:
        """Upload a HARM Core Segment to the API and associate with a Core

        :param core_id: parent Core ID
        :type core_id: UUID
        :param new_core_segment: core segment object to be uploaded
        :type new_core_segment: CoreSegment
        :return: Core segment as processed by the server
        :rtype: CoreSegment
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                segment_url = self.core_url / str(core_id) / "segment"
                r = session.post(segment_url, 
                                data=new_core_segment.model_dump_json(exclude_unset=True))
                if r.ok:
                    return CoreSegment(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def list_cores(self,
                   dataset_id: UUID | None = None,
                   record_hash: str | None = None,
                   active_core: bool | None = None, 
                   location_id: UUID | None = None,
                   datatype_id: UUID | None = None, 
                   core_type: Literal["ice", "sediment", "other"] | None = None,) -> List[Core]:
        """Get all of the HARM Cores on the server

        :return: List of HARM Core objects
        :rtype: List[Core]
        """
        if dataset_id is not None:
            dataset_id = str(dataset_id)
        if location_id is not None:
            location_id = str(location_id)
        if datatype_id is not None:
            datatype_id = str(datatype_id)
        params = {
            "dataset_id": dataset_id,
            "record_hash": record_hash,
            "active_core": active_core,
            "location_id": location_id,
            "datatype_id": datatype_id,
            "core_type": core_type
        }
        params = {x:y for x, y in params.items() if y is not None}
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                r = session.get(self.core_url,
                                params=params)
                if r.ok:
                    return [Core(**x) for x in r.json()]
                else: 
                    eval_non_ok_return(r.status_code)
    def list_core_segments(self, \
                           core_id: UUID | None = None,
                           dataset_id: UUID | None = None, 
                           record_hash: str | None = None, 
                           location_id: UUID | None = None,
                           datatype_id: UUID | None = None,
                           active_segments: bool | None = None,) -> List[CoreSegment]:
        """List HARM Core Segments for a HARM Core

        :param core_id: core_id of the parent HARM Core, defaults to None
        :type core_id: UUID | None, optional
        :return: List of HARM Core Segments for HARM Core
        :rtype: List[CoreSegment]
        """
        if core_id is not None:
            core_id = str(core_id)
        if dataset_id is not None:
            dataset_id = str(dataset_id)
        if location_id is not None:
            location_id = str(location_id)
        if datatype_id is not None:
            datatype_id = str(datatype_id)
        params = {
            "dataset_id": dataset_id,
            "record_hash": record_hash,
            "location_id": location_id,
            "datatype_id": datatype_id,
            "active_segments": active_segments
        }
        params = {x: y for x, y in params.items()}
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                segment_url = self.core_url / core_id / "segment"
                r = session.get(segment_url)
                if r.ok:
                    return [CoreSegment(**x) for x in r.json()]
                else: 
                    eval_non_ok_return(r.status_code)
    def get_core(self, core_id: UUID) -> Core:
        """Get an individual HARM Core from the server

        :param core_id: core_id of the desired HARM Core, defaults to None
        :type core_id: UUID | None, optional
        :return: HARM Core object
        :rtype: Core
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                core_url = self.core_url / str(core_id)
                r = session.get(core_url)
                if r.ok:
                    return Core(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def get_core_segment(self, core_id: UUID, core_segment_id: UUID) -> CoreSegment:
        """Get an individual HARM Core Segment from the API

        :param core_id: core_id of the parent HARM Core
        :type core_id: UUID
        :param core_segment_id: core_segment_id of the desired HARM Core Segment
        :type core_segment_id: UUID
        :return: HARM Core Segment
        :rtype: CoreSegment
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                segment_url = self.core_url / str(core_id) / "segment" / str(core_segment_id)
                r = session.get(segment_url)
                if r.ok:
                    return CoreSegment(**r.json())
                else: 
                    eval_non_ok_return(r.status_code)
    def delete_core(self, core_id: UUID) -> None:
        """Delete a HARM Core from the API

        :param core_id: core_id of the HARM Core to be deleted
        :type core_id: UUID
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                core_url = self.core_url / str(core_id)
                r = session.delete(core_url)
    def delete_core_segment(self, core_id: UUID, core_segment_id: UUID) -> None:
        """Delete a HARM Core Segment from the API

        :param core_id: core_id of the parent HARM Core
        :type core_id: UUID
        :param core_segment_id: core_segment_id of the HARM Core Segment to be deleted
        :type core_segment_id: UUID
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                segment_url = self.core_url / str(core_id) / "segment" / str(core_segment_id)
                r = session.delete(segment_url)
    def assign_core_segment_to_record_hash(self, core_segment_id: UUID, record_hash: str) -> None:
        """Assign a HARM Core Segment to a record hash

        :param core_segment_id: core_segment_id of the HARM Core Segment to be assigned to the record
        :type core_segment_id: UUID
        :param record_hash: Record hash the HARM Core Segment will be associated to
        :type record_hash: str
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                segment_url = self.core_url / "segment" / str(core_segment_id) / "assign" / record_hash
                r = session.post(segment_url)
    def remove_core_segment_from_record_hash(self, core_segment_id: UUID, record_hash: str) -> None:
        """Remove a HARM Core Segment from a record hash

        :param core_segment_id: core_segment_id of the HARM Core Segment to be disassicated from
        :type core_segment_id: UUID
        :param record_hash: Record hash the HARM Core Segment will no longer be associated with
        :type record_hash: str
        """
        with self.p2fclient.sessionmaker() as session:
            if self.p2fclient.health_check(session=session):
                segment_url = self.core_url / "segment" / str(core_segment_id) / "remove" / record_hash
                r = session.delete(segment_url)