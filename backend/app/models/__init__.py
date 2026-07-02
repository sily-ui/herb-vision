# 导入所有模型，以便 Base.metadata.create_all 能发现它们
from app.models.herb import Herb
from app.models.user import User
from app.models.identify_record import IdentifyRecord
from app.models.feedback import Feedback
