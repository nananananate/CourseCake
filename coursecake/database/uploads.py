# uploads courses

from sqlalchemy.orm import Session

from ..scrapers.course import Course
from ..scrapers.course_scraper import CourseScraper

from . import crud, models


def update_all(db: Session, term_id: str = "2020-FALL-1", testing: bool = False):
    term_args = term_id.split("-")

    # check if term_id is fully specified
    # if not, fill in assumed values
    if len(term_args) < 3:
        term_id += "-1"

    universities = ["uci", "ucsc", "calpoly"]
    scrapers = CourseScraper()

    for university in universities:
        scraper = scrapers.get_scraper(university, term_id)
        scraper.get_classes(testing=testing)
        courses = list(scraper.courses.values())
        upload_courses(db, term_id, testing, university, courses)


def upload_courses(
    db: Session, term_id: str, testing: bool, university: str, courses: list
):
    """
    uploads courses and classes
    """
    classes = list()
    for course in courses:
        classes.extend(course.classes)

    crud.add_university(db, university)
    crud.bulk_merge_courses(db, university, term_id, courses)
    crud.bulk_merge_classes(db, university, term_id, classes)
