from tortoise import Model, fields


class MyMarkdown(Model):
    """内容表"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    content = fields.CharField(max_length=10000)
    last_modify = fields.FloatField()
    create_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)
# content = fields.CharField(max_length=500)
