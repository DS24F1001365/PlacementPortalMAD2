from celery import Celery

from flask import Flask
from config import Config
from models import db

import csv
import os
from models import (
    db,
    User,
    Student,
    Application,
    PlacementDrive,
    Company
)

from datetime import date, timedelta
from mail_utils import send_email


EXPORT_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "exports"
)

os.makedirs(EXPORT_FOLDER, exist_ok=True)

celery = Celery(
    "placement_portal",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

from celery.schedules import crontab


flask_app = Flask(__name__)

flask_app.config.from_object(Config)

db.init_app(flask_app)

celery.conf.update(
    result_expires=3600
)
celery.conf.beat_schedule = {

    "daily-placement-reminders": {
        "task": "celery_app.send_daily_reminders",
        "schedule": crontab(hour=9, minute=0)
    },
    "monthly-placement-report":{
        "task":"celery_app.send_monthly_report",
        "schedule":crontab(day_of_month=1, hour=9, minute=0)

}
}
#REPLACE SHEDULE VALUE WITH crontab(hour=9, minute=0) or 10.0
celery.conf.timezone = "Asia/Kolkata"


@celery.task
def hello():
    print("Hello from Celery!")
    return "Task Completed!"

@celery.task
def export_student_applications(student_id):

    with flask_app.app_context():

        student = Student.query.get(student_id)
        filename = f"student_{student_id}_applications.csv"
        filepath = os.path.join(EXPORT_FOLDER, filename)
        applications = Application.query.filter_by(student_id=student_id).all()
        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Student ID",
                "Company",
                "Job Title",
                "Specialization",
                "Application Status",
                "Offer Status",
                "Applied On"
            ])

            for application in applications:
                drive = PlacementDrive.query.get(application.drive_id)

                company = Company.query.get(drive.company_id)

                writer.writerow([
                    student.id,
                    company.user.name,
                    drive.job_title,
                    drive.specialization,
                    application.application_status,
                    application.offer_status,
                    application.applied_on.strftime("%Y-%m-%d")
                ])
        return filename


@celery.task
def send_daily_reminders():

    with flask_app.app_context():
        today = date.today()
        reminder_deadline = today + timedelta(days=365)
        students = Student.query.all()
        for student in students:
            print("-------------------------")
            print("Student:", student.user.name)
            if (
                not student.is_active
                or student.is_placed
                or student.user.blacklist_status
            ):
                continue

            reminder_text = ""

            drives = PlacementDrive.query.filter(
                PlacementDrive.status == "Approved",
                PlacementDrive.deadline >= today,
                PlacementDrive.deadline <= reminder_deadline
            ).all()

            for drive in drives:
                print("Checking:", drive.job_title)
                company = Company.query.get(drive.company_id)
                if company.approval_status != "Approved":
                    print("Company not approved")
                    continue

                branches = [branch.strip() for branch in drive.eligible_branches.split(",")]

                if student.branch not in branches:
                    print("Branch mismatch")
                    continue
                if student.year < drive.eligible_year:
                    print("Year mismatch")
                    continue
                if student.cgpa < drive.minimum_cgpa:
                    print("CGPA mismatch")
                    continue

                already_applied = Application.query.filter_by(
                    student_id=student.id,
                    drive_id=drive.id
                ).first()

                if already_applied:
                    print("Already applied")
                    continue

                reminder_text += f"""
                <hr>
                <b>Company :</b> {company.user.name}<br>
                <b>Role :</b> {drive.job_title}<br>
                <b>Specialization :</b> {drive.specialization}<br>
                <b>Deadline :</b> {drive.deadline}<br>
                """

            if reminder_text:

                body = f"""
                <h2>Placement Drive Reminder</h2>
                Hello {student.user.name},
                <br><br>
                The following placement drives are closing within the next 3 days.
                <br><br>
                {reminder_text}
                <br><br>
                Please apply before the deadline.
                <br><br>
                Placement Portal
                """
                print("EMAIL WILL BE SENT")
                print(reminder_text)

                send_email(
                    student.user.email,
                    "Placement Drive Reminder",
                    body
                )

    return "Daily Reminder Completed"

@celery.task
def send_monthly_report():

    with flask_app.app_context():

        total_drives = PlacementDrive.query.filter_by(
            status="Closed"
        ).count()

        total_applications = Application.query.count()

        total_selected = Application.query.filter_by(
            application_status="Selected"
        ).count()

        body = f"""
        <html>

        <body>

        <h2>Monthly Placement Report</h2>

        <hr>

        <p>

        <b>Total Drives Conducted :</b>

        {total_drives}

        </p>

        <p>

        <b>Total Applications :</b>

        {total_applications}

        </p>

        <p>

        <b>Total Students Selected :</b>

        {total_selected}

        </p>

        <hr>

        Placement Portal

        </body>

        </html>
        """

        admin = User.query.filter_by(
            role="admin"
        ).first()

        send_email(

            admin.email,

            "Monthly Placement Report",

            body

        )

    return "Monthly Report Sent"