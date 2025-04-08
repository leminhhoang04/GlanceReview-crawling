import openreview
import requests

class OpenReviewClient:
    def __init__(self, version):
        assert version in [1, 2], 'Invalid version'
        self._version = version
        self._client = self._get_client(version)

    def get_all_venues(self):
        """
        Get all venues (data) from OpenReview API.
        """
        venues = self._client.get_group(id='venues').members
        venues.sort(reverse=True)
        return venues

    def get_conference_notes(self, venue, active=False):
        """
        Get all notes of a conference (data) from OpenReview API.
        If results are not final (accepted), you should set active=True.
        not active = accepted
        """
        if self._version == 1:
            if active:
                notes = self._client.get_all_notes(invitation=f'{venue}/-/Blind_Submission')
            else:
                notes = self._client.get_all_notes(invitation=f'{venue}/-/Submission')
        else:
            if active:
                venue_group = self._client.get_group(venue)
                if venue_group.content is None:
                    return []
                under_review_id = venue_group.content['submission_venue_id']['value']
                notes = self._client.get_all_notes(content={'venueid': under_review_id})
            else:
                notes = self._client.get_all_notes(content={'venueid': venue} )
        return notes

    def get_attachment(self, note_id, attachment_name):
        """
        Get attachment (e.g., PDF) of a note from OpenReview API.
        """
        return self._client.get_attachment(note_id, attachment_name)

    def get_pdf(self, note_id):
        """
        Get PDF of a note_id from OpenReview API.
        """
        return self._client.get_pdf(note_id)

    def _get_client(self, version: int):
        if version == 1:
            # API V1
            _client_v1 = openreview.Client(
                baseurl='https://api.openreview.net',
            )
            return _client_v1
        else:
            # API V2
            _client_v2 = openreview.api.OpenReviewClient(
                baseurl='https://api2.openreview.net',
            )
            return _client_v2