import unittest
from QuantumPathQSOAPySDK import QSOAPlatform


##################_____GET ENVIRONMENTS_____##################
class Test_GetEnvironments(unittest.TestCase):

    # GET ENVIRONMENTS
    def test_getEnvironments(self):
        qsoa = QSOAPlatform()

        environments = qsoa.getEnvironments()

        self.assertIsInstance(environments, dict)
        self.assertEqual(environments, {'default-environments': {'pro': 'https://qsoa.quantumpath.app:8443/api/'},
                                        'custom-environments': {}
        })
    
    '''
    CREATE custom = url IN .QPATH CONFIG FILE
    '''
    # GET ENVIRONMENTS CUSTOM ENVIRONMENT   
    # def test_getEnvironments_customEnvironment(self):
    #     qsoa = QSOAPlatform()

    #     environments = qsoa.getEnvironments()

    #     self.assertIsInstance(environments, dict)
    #     self.assertEqual(environments, {'default-environments': {'pro': 'https://qsoa.quantumpath.app:8443/api/'},
    #                                     'custom-environments': {'custom': 'url'}
    #     })


##################_____GET ACTIVE ENVIRONMENT_____##################
class Test_GetActiveEnvironment(unittest.TestCase):

    # GET ACTIVE ENVIRONMENT
    def test_getActiveEnvironment(self):
        qsoa = QSOAPlatform()

        activeEnvironment = qsoa.getActiveEnvironment()

        self.assertIsInstance(activeEnvironment, tuple)
        self.assertEqual(activeEnvironment, ('default-environments', 'pro'))


##################_____SET ACTIVE ENVIRONMENT_____##################
class Test_SetActiveEnvironment(unittest.TestCase):

    # SET ACTIVE ENVIRONMENT
    def test_setActiveEnvironment(self):
        qsoa = QSOAPlatform()

        setActiveEnvironment = qsoa.setActiveEnvironment('pro')

        self.assertIsInstance(setActiveEnvironment, tuple)
        self.assertEqual(setActiveEnvironment, ('default-environments', 'pro'))
    
    # SET ACTIVE ENVIRONMENT qSOATargetURL SLASH
    def test_setActiveEnvironment_qSOATargetURL_slash(self):
        qsoa = QSOAPlatform()

        setActiveEnvironment = qsoa.setActiveEnvironment('custom', 'url/', True)

        customEnvironments = qsoa.getEnvironments()['custom-environments']

        self.assertEqual(customEnvironments, {'custom': ('url/', True)})
        self.assertIsInstance(setActiveEnvironment, tuple)
        self.assertEqual(setActiveEnvironment, ('custom-environments', 'custom'))

    # SET ACTIVE ENVIRONMENT qSOATargetURL NO SLASH
    def test_setActiveEnvironment_qSOATargetURL_noSlash(self):
        qsoa = QSOAPlatform()

        setActiveEnvironment = qsoa.setActiveEnvironment('custom', 'url', True)

        customEnvironments = qsoa.getEnvironments()['custom-environments']

        self.assertEqual(customEnvironments, {'custom': ('url/', True)})
        self.assertIsInstance(setActiveEnvironment, tuple)
        self.assertEqual(setActiveEnvironment, ('custom-environments', 'custom'))

    # SET ACTIVE ENVIRONMENT qSOATargetURL OVERRIDE
    def test_setActiveEnvironment_qSOATargetURL_override(self):
        qsoa = QSOAPlatform()
        qsoa.setActiveEnvironment('custom', 'url')

        setActiveEnvironment = qsoa.setActiveEnvironment('custom', 'url2', True)

        customEnvironments = qsoa.getEnvironments()['custom-environments']

        self.assertEqual(customEnvironments, {'custom': ('url2/', True)})
        self.assertIsInstance(setActiveEnvironment, tuple)
        self.assertEqual(setActiveEnvironment, ('custom-environments', 'custom'))

    # BAD ARGUMENT environmentName
    def test_setActiveEnvironment_badArgument_environmentName(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.setActiveEnvironment('environmentName')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT qSOATargetURL DEFAULT
    def test_setActiveEnvironment_badArgument_qSOATargetURL_default(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.setActiveEnvironment('pro', 'url', True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE environmentName
    def test_setActiveEnvironment_badArgumentType_environmentName(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.setActiveEnvironment(0)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE qSOATargetURL
    def test_setActiveEnvironment_badArgumentType_qSOATargetURL(self):
        qsoa = QSOAPlatform()

        try:
            qsoa.setActiveEnvironment('custom', 'url2', 'qSOATargetURL')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()