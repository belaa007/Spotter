using System;
using System.Runtime.Serialization;

namespace SpotterDataTransferObject
{
    [DataContract]
    public class UpdateResult
    {
        [DataMember]
        public String S { get; set; }
    }
}
