﻿using System;
using System.Threading.Tasks;
using Amazon;
using Amazon.Runtime;
using Amazon.S3;
using Amazon.S3.Model;

namespace BucketACLExample
{
    public class BucketACL
    {
        public static async Task Main()
        {
            const string newBucketName = "doc-example-bucket";
            const string accessKey = "AKIARV72Q7H2VQUFRREH"; // Replace with your IAM user's access key
            const string secretKey = "qEtdLXgvqEF2uoAdyq4b7cPo7dUv+ZxQJ2AA9cv1"; // Replace with your IAM user's secret access key
            const string regionName = "us-east-1"; // Replace with your desired AWS region

            var credentials = new BasicAWSCredentials(accessKey, secretKey);
            var region = RegionEndpoint.GetBySystemName(regionName);

            IAmazonS3 client = new AmazonS3Client(credentials, region);

            var success = await CreateBucketUseCannedACLAsync(client, newBucketName);

            if (success)
            {
                Console.WriteLine("Amazon S3 bucket created.");
                var aclList = await GetACLForBucketAsync(client, newBucketName);
                if (aclList.Grants.Count > 0)
                {
                    DisplayACL(aclList);
                }
            }
        }

        public static async Task<bool> CreateBucketUseCannedACLAsync(IAmazonS3 client, string newBucketName)
        {
            try
            {
                var putBucketRequest = new PutBucketRequest()
                {
                    BucketName = newBucketName,
                    CannedACL = S3CannedACL.LogDeliveryWrite,
                };

                PutBucketResponse putBucketResponse = await client.PutBucketAsync(putBucketRequest);

                return putBucketResponse.HttpStatusCode == System.Net.HttpStatusCode.OK;
            }
            catch (AmazonS3Exception ex)
            {
                Console.WriteLine($"Amazon S3 error: {ex.Message}");
            }

            return false;
        }

        public static async Task<S3AccessControlList> GetACLForBucketAsync(IAmazonS3 client, string newBucketName)
        {
            GetACLResponse getACLResponse = await client.GetACLAsync(new GetACLRequest
            {
                BucketName = newBucketName,
            });

            return getACLResponse.AccessControlList;
        }

        public static void DisplayACL(S3AccessControlList acl)
        {
            Console.WriteLine($"\nOwner: {acl.Owner}");

            acl.Grants.ForEach(g =>
            {
                Console.WriteLine($"{g.Grantee}, {g.Permission}");
            });
        }
    }
}
