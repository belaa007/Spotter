using System;
using System.Collections.Generic;
using System.Runtime.Serialization;

namespace SpotterDataTransferObject
{
    [DataContract]
    public class FPingParameter
    {
        [DataMember]
        public IList<String> SList { get; set; }
    }
}