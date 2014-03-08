using System;
using System.Runtime.Serialization;

namespace SpotterDataTransferObject
{
    [DataContract]
    public class PingResult
    {
        [DataMember]
        public String S { get; set; }
    }
}