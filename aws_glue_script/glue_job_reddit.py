import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import concat_ws
from awsglue import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1723681317504 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": '"', "withHeader": True, "separator": ","}, connection_type="s3", format="csv", connection_options={"paths": ["s3://reddit-de-airscholar/raw/reddit_data_20240815.csv"], "recurse": True}, transformation_ctx="AmazonS3_node1723681317504")

# convert dynamic frame to dataframe
df = AmazonS3_node1723681317504.toDF()
# print(df.columns)

print(df.columns)
# print(df.head())
# print(df.keys())
# concate 3 columns to single column 
# df_combined = df.withColumn("ESS_Updated", concat_ws('-', df['col8'], df['col9'], df['col10']))
# df_combined = df_combined.drop('col8', 'col9', 'col10')
df_combined = df.withColumn("ESS_Updated", concat_ws('-', df['edited'], df['spoiler'], df['stickied']))
df_combined = df_combined.drop('edited', 'spoiler', 'stickied')
# convert df back to dynamic frame 
s3_bucket_node_combined = DynamicFrame.fromDF(df_combined, glueContext, 's3_bucket_node_combined')


# Script generated for node Amazon S3
AmazonS3_node1723681321036 = glueContext.write_dynamic_frame.from_options(frame=s3_bucket_node_combined, connection_type="s3", format="csv", connection_options={"path": "s3://reddit-de-airscholar/transformed/", "partitionKeys": []}, transformation_ctx="AmazonS3_node1723681321036")

job.commit()