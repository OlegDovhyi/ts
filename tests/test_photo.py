import unittest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
import sys
import os
from src.database.models import Photo
from src.repository.photo import remove_photo, update_description, see_photo

sys.path.append(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))


class TestPhotoRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = AsyncMock(spec=AsyncSession())

    async def tearDown(self) -> None:
        del self.session

    async def test_remove_photo(self):
        photo_id = 1
        current_user_id = 2
        mock_photo = Photo(id=photo_id, user_id=current_user_id)
        self.session.execute.return_value.scalar_one_or_none.return_value = mock_photo
        self.session.begin.return_value.__aenter__.return_value = None

        result = await remove_photo(photo_id, current_user_id, self.session)

        self.assertEqual(result, mock_photo)
        self.session.execute.assert_called_once_with(
            Photo.__table__.select().where(
                (Photo.id == photo_id) & (Photo.user_id == current_user_id)
            )
        )
        self.session.delete.assert_called_once_with(mock_photo)

    async def test_update_description(self):
        photo_id = 1
        current_user_id = 2
        new_description = "New Description"
        mock_photo = Photo(id=photo_id, user_id=current_user_id)
        self.session.execute.return_value.scalar_one_or_none.return_value = mock_photo
        self.session.commit.return_value = None
        self.session.refresh.return_value = None

        result = await update_description(photo_id, new_description, current_user_id, self.session)

        self.assertEqual(result, mock_photo)
        self.session.execute.assert_called_once_with(
            Photo.__table__.select().where(
                (Photo.id == photo_id) & (Photo.user_id == current_user_id)
            )
        )
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(mock_photo)

    async def test_see_photo(self):
        photo_id = 1
        mock_photo = Photo(id=photo_id)
        self.session.execute.return_value.scalar_one_or_none.return_value = mock_photo

        result = await see_photo(photo_id, self.session)

        self.assertEqual(result, mock_photo)
        self.session.execute.assert_called_once_with(
            Photo.__table__.select().where(Photo.id == photo_id)
        )

if __name__ == '__main__':
    unittest.main()
