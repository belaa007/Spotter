using System;
using System.Runtime.Serialization;

namespace SpotterDataTransferObject
{
    [DataContract]
    public class FPingResult
    {
        [DataMember]
        public String S { get; set; }
    }
}