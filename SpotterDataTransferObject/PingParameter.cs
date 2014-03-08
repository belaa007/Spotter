using System;
using System.Runtime.Serialization;

namespace SpotterDataTransferObject
{
    [DataContract]
    public class PingParameter
    {
        [DataMember]
        public String S { get; set; }   
    }
}