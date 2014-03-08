using System;
using System.Runtime.Serialization;

namespace SpotterDataTransferObject
{
    [DataContract]
    public class UpdateParameter
    {
        [DataMember]
        public String S { get; set; }
    }
}
