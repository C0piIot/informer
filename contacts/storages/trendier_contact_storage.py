import mysql.connector
from contacts.models import Contact
from accounts.models import EmailChannel

class TrendierContactStorage:
    connection = None
    select = """SELECT 
                i_user_id AS `key`,
                s_user_name AS username,
                s_user_email AS email,
                s_user_first_name AS first_name,
                s_user_last_name AS last_name
            FROM tbl_users
            JOIN tbl_users_data ON fk_i_user_id=i_user_id"""

    @classmethod
    def get_connection(cls):
        if not cls.connection:
            cls.connection =  mysql.connector.connect(
              host ="informer_mysql",
              user ="root",
              passwd ="",
              database="gotrendier_co"
            )
        return cls.connection

    @classmethod
    def row_to_instance(cls, row, email_channel):
        channel_data={}
        if email_channel :
            channel_data[str(email_channel.pk)] = { 'email': row.pop('email') }
        return Contact(
            key=row.pop('key'),
            name=row.pop('username'),
            channel_data=channel_data,
            contact_data=row,
        )
        return

    @classmethod
    def get_contacts(cls, environment, start_key=None, amount=50, **filters):
        connection = cls.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(cls.select + """
            WHERE i_user_id > %s
            ORDER BY i_user_id
            LIMIT %s
        """, (start_key if start_key else 0, amount))
        
        email_channel = EmailChannel.objects.filter(site=environment.site).first()
            
        return [cls.row_to_instance(row, email_channel) for row in cursor.fetchall()]
   
        #TODO:falta environment  Contact.objects.filter(environment=environment)
        
        
    @classmethod
    def get_contact(cls, environment, key):
        connection = cls.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(cls.select + " WHERE i_user_id = %s", (key,))
        email_channel = EmailChannel.objects.filter(site=environment.site).first()
        return cls.row_to_instance(cursor.fetchone(), email_channel)
        

    @classmethod
    def save_contact(cls, environment, contact):
        pass

    @classmethod
    def delete_contact(cls, environment, key):
        pass
